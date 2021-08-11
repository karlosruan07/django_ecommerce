from django.db import models
from catalog.models import Produto

class Carrinho(models.Model):
    chave_carrinho = models.CharField('Chave do Carrinho', max_length=40, db_index=True)
    produto = models.ForeignKey(Produto, verbose_name='Produto',on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1, verbose_name='Quantidade')
    preco = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Preço')

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'

    def __str__(self):
        return '{}, [{}]'.format(self.produto, self.quantidade)


