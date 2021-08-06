
from django import forms
from django.db import models
from django.forms import fields
from .models import Contato

#formulario de cadastro
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.core.mail import send_mail
from django.conf import settings

class FormularioContato(forms.ModelForm):
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
        
class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(max_length=100)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        e = self.cleaned_data['email']#pega o objeto email da lista da classe User acima
        if User.objects.filter(email=e).exists():
            raise ValidationError(f"O email {e} já existe.")
        return e

