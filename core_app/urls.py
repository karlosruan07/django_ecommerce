
from django.urls import path
from . import views


urlpatterns = [
    
    path('contatos/', views.contatos, name='contatos'),
    path('lista_produtos/', views.lista_produtos, name='lista_produtos'),
]
