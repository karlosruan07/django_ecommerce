
from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.CadastrarUsuario.as_view(), name='cadastrar'),

]

