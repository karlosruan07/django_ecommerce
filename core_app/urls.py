
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('contatos/', views.contatos, name='contatos'),
    path('lista_produtos/', views.lista_produtos, name='lista_produtos'),
    path('produto/', views.produto, name='produto'),
]
