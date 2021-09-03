
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.views.generic import RedirectView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.models import Produto
from .models import Carrinho, Pedido

from django.forms import modelform_factory

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


