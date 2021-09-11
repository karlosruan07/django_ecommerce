
from django_ecommerce.settings import PAYPAL_EMAIL
from django.forms.models import modelformset_factory
from django.http import response, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse
from django.views import generic
from django.views.generic import RedirectView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.models import Produto
from .models import Carrinho, Pedido

from django.forms import modelform_factory

from django.views.decorators.csrf import csrf_exempt
from pagseguro import PagSeguro
from django.conf import settings

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED#armazena o valor quando a transação está completada
from paypal.standard.ipn.signals import valid_ipn_received#os sinais ficam aqui nessa biblioteca

class CriarItemCarrinho(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        produto = get_object_or_404(Produto, slug=self.kwargs['slug'])

        if self.request.session.session_key is None:#se ainda não estiver usando a seção, então o django força a criar uma.
            self.request.session.save()#salva a seção

        item_carrinho, criado = Carrinho.objects.adicionar_item(self.request.session.session_key, produto)
        
        if criado:
            messages.success(self.request, 'Produto Adiconado com sucesso')

        else:
            messages.success(self.request, 'Produto Atualizado com sucesso')

        return reverse_lazy('carrinho')


class ListarItensCarrinho(TemplateView):
    
    template_name = 'checkout/carrinho.html'

    def get_formset(self, clear=False):

        FormularioItemCarrinho = modelformset_factory(
            Carrinho, fields=('quantidade',), can_delete=True, extra=0
        )

        session_key = self.request.session.session_key #pega a sessão atual

        if session_key:

            if clear:
                formset = FormularioItemCarrinho(
                queryset=Carrinho.objects.filter(chave_carrinho=session_key) #filtra os objetos da sessão atual
            )

            else:
                formset = FormularioItemCarrinho(
                queryset=Carrinho.objects.filter(chave_carrinho=session_key),
                data=self.request.POST or None  #filtra os objetos da sessão atual
            )

        else:

            formset = FormularioItemCarrinho(queryset=Carrinho.objects.none())

        return formset

    def get_context_data(self, **kwargs):
        context = super(ListarItensCarrinho, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = self.get_context_data(**kwargs)

        if formset.is_valid():
            formset.save()
        
            messages.success(request, 'Carrinho atualizado com sucesso !!!')
            context['formset'] = self.get_formset(clear=True)
        
        return self.render_to_response(context)


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout/checkout.html'

    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key

        if session_key and Carrinho.objects.filter(chave_carrinho=session_key).exists():#verifica se há items no carrinho
            cart_items = Carrinho.objects.filter(chave_carrinho=session_key)#filtra os items do carrinho pela chave do carrinho da seção antiga
            pedido = Pedido.objects.criar_pedido(
                usuario=request.user, cart_items=cart_items
            )

        else:
            messages.success(request, 'Não há item no carrinho de comprar.')
            return redirect('carrinho')
        response = super(CheckoutView, self).get(request, *args, **kwargs)
        response.context_data['pedido'] = pedido
        return response


class ListaPedido(LoginRequiredMixin, generic.ListView):

    template_name = 'checkout/lista_pedidos.html'
    paginate_by = 5

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)


class DetalhePedido(LoginRequiredMixin, generic.DetailView):
    template_name = 'checkout/detalhe_pedido.html'
    model = Pedido
    context_object_name = 'pedido'

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)


class PagseguroView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pedido_pk = self.kwargs.get('pk')
        pedido = get_object_or_404(Pedido.objects.filter(usuario=self.request.user), pk=pedido_pk)
        pg = pedido.pagseguro()
        pg.redirect_url = HttpResponseRedirect(
            reverse('detalhe-pedido', args=[pedido.pk])
        )

        pg.notification_url = self.request.build_absolute_uri(
            reverse('notificacao-pagseguro')#adiciona a url de resposta da API caso o mercado pago queira se comunicar com a gente
        )

        response = pg.checkout()
        return response.payment_url


@csrf_exempt
def pagseguro_notification(request):
    codigo_notificacao = request.POST.get('notificationCode', None)#recebe o código do pagseguro 
    if codigo_notificacao:
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
        )
        dados_notificacao = pg.check_notification(codigo_notificacao)#veifica o código enviado
        status = dados_notificacao.status#status do pagseguro que é enviado
        referencia = dados_notificacao.reference#id do nosso pedido

        try:
            pedido = Pedido.objects.get(pk=referencia)#pedido com o id
        except Pedido.DoesNotExist:
            pass
        else:
            pedido.pagseguro_update_status(status)

    return response.HttpResponse('OK')
import paypal

class PaypalView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout/paypal.html'

    def get_context_data(self, **kwargs):
        context = super(PaypalView, self).get_context_data(**kwargs)
        pedido_pk = self.kwargs.get('pk')
        pedido = get_object_or_404(
            Pedido.objects.filter(usuario=self.request.user), pk=pedido_pk
        )
        paypal_dict = pedido.paypal()#este dicionário vem do método criado no model
        
        paypal_dict['return_url'] = self.request.build_absolute_uri(#url que o paypal vai redirecionar o usuário depos de realizar o pagamento
            reverse('meus-pedidos')
        )
        paypal_dict['cancel_return'] = self.request.build_absolute_uri(
            reverse('meus-pedidos')
        )

        paypal_dict['notify_url'] = self.request.build_absolute_uri(
            reverse('paypal-ipn')
        )

        context['form'] = PayPalPaymentsForm(initial=paypal_dict)
        return context
        

def notificacao_paypal(sender, **kwargs):
    ipn_obj = sender #objeto da notificação
    if ipn_obj.payment_status == ST_PP_COMPLETED and ipn_obj.receiver_email == settings.PAYPAL_EMAIL:#verifica se o status da transação é comcluída e se o email a mensagem é o mesmo dos settings
        try:
            pedido = Pedido.objects.get(pk=ipn_obj.invoice)
            pedido.complete()#esta função esta nos models e muda o status de um determinado pedido
        except Pedido.DoesNotExist:
            pass

valid_ipn_received.connect(notificacao_paypal)#quando um sinal é recebido ele chama essa função
