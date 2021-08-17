
from django.db import models
from catalog.models import Produto

from django.conf import settings


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


class Pedido(models.Model):

    STATUS_ = (
        (0, 'Aguardando Pagamento'),
        (1, 'Concluída'),
        (2, 'Cancelado'),
    )

    OPCAO_PAGAMENTO_ = (
        ('pagseguro', 'PagSeguro'),
        ('paypal', 'Paypal'),
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
    status = models.IntegerField('Situação', choices=STATUS_, default=0, blank=True)
    opcao_pagamento = models.CharField('Opção de pagamentos', choices=OPCAO_PAGAMENTO_, max_length=10 )
    criado = models.DateTimeField('Criado em', auto_now_add=True)#é adicionado no momento da criação, não pode ser alterado
    modificado = models.DateTimeField('Modificado em', auto_now=True)#é adicionado no momento da modificação, pode ser alterado

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return 'Pedido {}'.format(self.pk)


class ItensPedido(models.Model):

    pedido = models.ForeignKey(Pedido, verbose_name='Pedido', related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, verbose_name='Produto',on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1, verbose_name='Quantidade')
    preco = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Preço')

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'

    def _str__(self):
        return '{}, {}'.format(self.pedido, self.produto)


def post_save_cart_item(instance, **kwargs):#quando for salvar um dado, ele vai chamar essa função para verificação
    if instance.quantidade < 1:
        instance.delete()

models.signals.post_save.connect(
    post_save_cart_item, sender=Carrinho, dispatch_uid='post_save_cart_item'
)
 
