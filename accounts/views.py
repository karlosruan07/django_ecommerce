
from django.urls import reverse_lazy

from .models import User
from .forms import FormularioAdmin

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class CadastrarUsuario(generic.CreateView):
    model = User
    template_name = 'accounts/registro.html'
    form_class = FormularioAdmin
    success_url = reverse_lazy('login')


class EditarDadosUsuario(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'accounts/editar_dados.html'
    fields = ['username', 'email']
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user
    


