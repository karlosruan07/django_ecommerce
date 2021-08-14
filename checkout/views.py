
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import RedirectView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy

from catalog.models import Produto
from .models import Carrinho

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

    def get_context_data(self, **kwargs):
        context = super(ListarItensCarrinho, self).get_context_data(**kwargs)
        FormularioItemCarrinho = modelformset_factory(
            Carrinho, fields=('quantidade',), can_delete=True, extra=0
        )
        session_key = self.request.session.session_key

        if session_key:
            context['formset'] = FormularioItemCarrinho(
                queryset=Carrinho.objects.filter(chave_carrinho=session_key)
            )
        else:
            context['formset'] = FormularioItemCarrinho(
                queryset=Carrinho.objects.none()
            )
        return context


