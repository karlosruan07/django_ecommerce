
from django.urls import path
from . import views
from .views import Lista_Produtos, ListaProdutoCategoria, DetalheProduto

urlpatterns = [
    path('adicionar-produto', views.AdicionarProduto.as_view(), name='adicionar-produto'),
    path('', views.Lista_Produtos.as_view(), name='index'),#todos os produtos
    path('produtos/<str:slug>/', views.ListaProdutoCategoria.as_view(), name='lista-produto-categoria'),#filtro pela categoria
    path('produto/<str:slug>/', views.DetalheProduto.as_view(), name='detalhe-produto'),#apenas um produto
]
