
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from .models import Produto, Categoria


####  IMPORT DAS CLASSES GENÉRICAS  ####

from django.views import generic


class AdicionarProduto(generic.CreateView):
    template_name = 'catalog/form.html'
    model = Produto
    fields = ['nome', 'descricao', 'preco', 'slug', 'categoria']
    success_url = reverse_lazy('index')


class Lista_Produtos(generic.ListView):
    model = Produto
    template_name = 'catalog/lista_produtos.html'
    context_object_name = 'produtos'  #renomeando a variável que contem a lista de objetos que irá para o template
    paginate_by = 4 #vai para o template a variável paginator e a pag_obj
    

class DetalheProduto(generic.DeleteView):
    model = Produto
    template_name = 'catalog/produto.html'
    context_object_name = 'produto'
    

class ListaProdutoCategoria(generic.ListView):
    model = Produto
    template_name = 'catalog/filtro_cat_prod.html'
    context_object_name = 'lista_produtos'
    paginate_by = 2

    def get_queryset(self):
        #categoria = get_object_or_404(Categoria, slug=self.kwargs['slug'])
        context =  Produto.objects.filter(categoria__slug=self.kwargs['slug'])
        return context
    
    def get_context_data(self, **kwargs):
        context = super(ListaProdutoCategoria, self).get_context_data(**kwargs)
        context['categoria_atual'] = get_object_or_404(Categoria, slug=self.kwargs['slug'])
        return context
    





