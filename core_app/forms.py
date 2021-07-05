
from django import forms
from django.db import models
from django.forms import fields
from .models import Contato

from django.core.mail import send_mail
from django.conf import settings

class Form_contato(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email','titulo','mensagem']
    
    def send_email(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        titulo = self.cleaned_data['titulo']
        mensagem = self.cleaned_data['mensagem']
        mensagem = 'Nome: {}\nE-mail: {}\nMensagem: {}'.format(nome, email, mensagem)
            
        send_mail(titulo, mensagem, settings.DEFAULT_FROM_EMAIL,
                ['karlosruan93@gmail.com']
                )
    

