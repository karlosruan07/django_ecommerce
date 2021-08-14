
from django.db import models
from django.shortcuts import redirect
from catalog.models import Produto


class GerenciadorCarrinho(models.Manager):
    
    def adicionar_item(self, chave_carrinho, produto):
        
        if self.filter(chave_carrinho=chave_carrinho, produto=produto).exists():
            criado = False
            item_carrinho = self.get(chave_carrinho=chave_carrinho, produto=produto)
            item_carrinho.quantidade = item_carrinho.quantidade + 1
            item_carrinho.save()

        else:
            criado = True
            item_carrinho = Carrinho.objects.create(
                chave_carrinho=chave_carrinho, produto=produto, preco=produto.preco
            )

        return item_carrinho, criado


class Carrinho(models.Model):

    chave_carrinho = models.CharField('Chave do Carrinho', max_length=40, db_index=True)
    produto = models.ForeignKey(Produto, verbose_name='Produto',on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1, verbose_name='Quantidade')
    preco = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Preço')

    objects = GerenciadorCarrinho()

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        unique_together = (('chave_carrinho', 'produto'))

    def __str__(self):
        return '{}, [{}]'.format(self.produto, self.quantidade)

