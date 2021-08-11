

from django.urls import path
from . import views

####  IMPORT DAS CLASSES GENÉRICAS  ####
from .views import ClasseTeste

urlpatterns = [
    
    path('contato/', views.contato, name='contato'),
    path('mensagens/', views.mensagens, name='mensagens'),
    
    ####  URLs DAS CLASSES GENÉRICAS  ####    
    path('teste/', views.teste, name='teste'),
    
]

