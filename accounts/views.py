
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .models import User
from .forms import FormularioAdmin


class CadastrarUsuario(generic.CreateView):
    model = User
    template_name = 'accounts/registro.html'
    form_class = FormularioAdmin
    success_url = reverse_lazy('login')

