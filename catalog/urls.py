
from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.produtos, name='index'),#todos os produtos
    path('produtos/<str:slug>/', views.lista_produto_categoria, name='produtos'),#filtro pela categoria
    path('produto/<str:slug>/', views.produto, name='produto'),#apenas um produto
]
