
from django import forms
from django.core.mail.message import forbid_multi_line_headers
from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse

from django.contrib import messages

from .forms import Form_contato

####  IMPORT DAS CLASSES GENÉRICAS  ####

from django.views.generic import TemplateView

####  IMPORT DAS CLASSES GENÉRICAS  ####

def mensagens(request):
    #mensagens = messages.success(request, 'Profile details updated.')
    mensagens = messages.add_message(request, messages.ERROR, 'Hello Word !')
    return render(request, 'arquivos_html/mensagens.html', mensagens)

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


def contato(request):
    sucesso = False
    
    form = Form_contato(request.POST or None)
    
    if form.is_valid():
        form.send_email()
        sucesso = True
        return redirect('index')
    
    titulo_forms = 'Envie uma mensagem para nós !'
    context = {
        'titulo_forms': titulo_forms ,
        'form' : form,
        'sucesso' : sucesso
    }
    
    return render(request, 'arquivos_html/forms.html', context)

def lista_produtos(request):
    return render(request, 'arquivos_html/lista_produtos.html')


####  USO DAS CLASSES GENÉRICAS  ####

class ClasseTeste(TemplateView):
    template_name = 'arquivos_html/index.html'
    
    