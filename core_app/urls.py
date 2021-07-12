
from django.http import request
from django.urls import path
from . import views

####  IMPORT DAS CLASSES GENÉRICAS  ####
from .views import ClasseTeste

urlpatterns = [
    
    path('contato/', views.contato, name='contato'),
    path('lista_produtos/', views.lista_produtos, name='lista_produtos'),
    path('mensagens/', views.mensagens, name='mensagens'),
    
    ####  URLs DAS CLASSES GENÉRICAS  ####    
    path('index/', ClasseTeste.as_view()),
    
]
