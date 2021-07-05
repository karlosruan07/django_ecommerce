
from django.urls import path
from . import views


urlpatterns = [
    
    path('contato/', views.contato, name='contato'),
    path('lista_produtos/', views.lista_produtos, name='lista_produtos'),
    path('mensagens/', views.mensagens, name='mensagens'),
    
    
]
