from django.db import models
from django.forms import widgets

class Contato(models.Model):
    nome = models.CharField('Nome', max_length=50, blank=False, null=False)
    email = models.EmailField('Email',max_length=50,blank=False, null=False)
    titulo = models.CharField('Titulo',max_length=255, blank=False, null=False)
    mensagem = models.TextField('Mensagem',blank=False, null=False)
