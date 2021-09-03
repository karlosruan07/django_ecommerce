
from django.urls import path
from . import views

urlpatterns = [

    path('carrinho/adicionar/<str:slug>/', views.CriarItemCarrinho.as_view(), name='adicionar-item-carrinho'),
    path('carrinho/', views.ListarItensCarrinho.as_view(), name='carrinho'),

    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('meus-pedidos/', views.ListaPedido.as_view(), name='meus-pedidos'),
    path('detalhe-pedido/<int:pk>/', views.DetalhePedido.as_view(), name='detalhe-pedido'),

]
