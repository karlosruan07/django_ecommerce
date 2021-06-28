
from django.shortcuts import render
from django.http import HttpResponse

def teste(request):
    items = [
        'Lorem Ipsum is simply dummy text of the printing and typesetting industry'
        ' Estou aprendendo django e python !'
    ]
    context = {
        "title":"django ecommerce",
        "items": items,
    }
    return render(request, 'arquivos_html/index.html', context)


def contatos(request):
    return render(request, 'arquivos_html/contatos.html')

def lista_produtos(request):
    return render(request, 'arquivos_html/lista_produtos.html')

