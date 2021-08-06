
from django.http import request
from django.urls import path
from django.urls.conf import include
from . import views

####  IMPORT DAS CLASSES GENÉRICAS  ####
from .views import ClasseTeste

urlpatterns = [
    
    path('contato/', views.contato, name='contato'),
    path('mensagens/', views.mensagens, name='mensagens'),
    
    ####  URLs DAS CLASSES GENÉRICAS  ####    
    path('index/', ClasseTeste.as_view()),
    
    #URLs do login, logout ...etc
    path('', include('django.contrib.auth.urls')),
    
    
]
