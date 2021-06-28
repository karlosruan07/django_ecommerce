
from django.urls import path
from . import views


urlpatterns = [
    path('', views.produtos, name='index'),
    
    path('produtos/<str:slug>/', views.categoria, name='produtos'),
    path('produto/<str:slug>/', views.produto, name='produto'),
]
