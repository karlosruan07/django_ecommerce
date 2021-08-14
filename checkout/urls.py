
from django.urls import path
from . import views

urlpatterns = [

    path('carrinho/adicionar/<str:slug>/', views.CriarItemCarrinho.as_view(), name='adicionar-item-carrinho'),
    path('carrinho/', views.ListarItensCarrinho.as_view(), name='carrinho')

]
