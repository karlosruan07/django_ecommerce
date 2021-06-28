from django.http.response import HttpResponse
from core_app.views import lista_produtos
from django.shortcuts import render
from .models import Produto, Categoria


def produtos(request):
    lista_produtos = Produto.objects.order_by('-criado')#ordena por ordem decrescente
    return render(request, 'catalog/lista_produtos.html', {'lista_produtos': lista_produtos})

def categoria(request, slug):
    categoria = Categoria.objects.get(slug=slug)
    context = {
        "titulo_atual" : categoria,
        "lista_produtos" : Produto.objects.filter(categoria=categoria)
    }

    return render(request, 'catalog/filtro_cat_prod.html', context)

def produto(request, slug):
    produto = Produto.objects.get(slug=slug)
    
    context = {
        "produto" : produto   
    }
    
    return render(request, 'catalog/produto.html', context)


