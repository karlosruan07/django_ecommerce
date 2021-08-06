
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy

from django.contrib import messages
from django.views import generic
from django.views.generic import CreateView

#forms de cadastro e registros ...
from .forms import FormularioContato

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
    
    form = FormularioContato(request.POST or None)
    
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



####  USO DAS CLASSES GENÉRICAS  ####

class ClasseTeste(TemplateView):
    template_name = 'arquivos_html/index.html'

