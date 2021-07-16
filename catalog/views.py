from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Produto, Categoria

####  IMPORT DAS CLASSES GENÉRICAS  ####

from django.views import generic

####  IMPORT DAS CLASSES GENÉRICAS  ####

class Lista_Produtos(generic.ListView):
    model = Produto
    template_name = 'catalog/lista_produtos.html'
    context_object_name = 'produtos'  #renomeando a variável que contem a lista de objetos que irá para o template
    paginate_by = 2 #vai para o template a variável paginator e a pag_obj
    
    
produtos = Lista_Produtos.as_view()


class ListaProdutoCategoria(generic.ListView):
    model = Produto
    template_name = 'catalog/filtro_cat_prod.html'
    context_object_name = 'lista_produtos'
    
    def get_queryset(self):
        #categoria = get_object_or_404(Categoria, slug=self.kwargs['slug'])
        return Produto.objects.filter(categoria__slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):
        context = super(ListaProdutoCategoria, self).get_context_data(**kwargs)
        context['categoria_atual'] = get_object_or_404(Categoria, slug=self.kwargs['slug'])
        return context
    
lista_produto_categoria = ListaProdutoCategoria.as_view()


def produto(request, slug):
    produto = Produto.objects.get(slug=slug)
    
    context = {
        "produto" : produto   
    }
    
    return render(request, 'catalog/produto.html', context)


