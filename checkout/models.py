
from django.db import models
from django.urls import conf
from catalog.models import Produto
from django.conf import settings

#imports do pagseguro

from pagseguro import PagSeguro


class GerenciadorCarrinho(models.Manager):
    
    def adicionar_item(self, chave_carrinho, produto):
        
        if self.filter(chave_carrinho=chave_carrinho, produto=produto).exists():
            criado = False
            item_carrinho = self.get(chave_carrinho=chave_carrinho, produto=produto)
            item_carrinho.quantidade = item_carrinho.quantidade + 1
            item_carrinho.preco = item_carrinho.preco * item_carrinho.quantidade
            item_carrinho.save()

        else:
            criado = True
            item_carrinho = Carrinho.objects.create(
                chave_carrinho=chave_carrinho, produto=produto, preco=produto.preco
            )

        return item_carrinho, criado

#CartItem
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


class GerenciadorPedido(models.Manager):

    def criar_pedido(self, usuario, cart_items):
        pedido = self.create(usuario=usuario)
        for item_carrinho in cart_items:
            items_pedido = ItensPedido.objects.create(
                pedido=pedido, quantidade=item_carrinho.quantidade, produto=item_carrinho.produto,
                preco=item_carrinho.preco
            )
        return pedido

class Pedido(models.Model):

    STATUS_ = (
        (0, 'Aguardando Pagamento'),
        (1, 'Concluída'),
        (2, 'Cancelado'),
    )

    OPCAO_PAGAMENTO_ = (
        ('pagseguro', 'PagSeguro'),
        ('paypal', 'Paypal'),
        ('deposito', 'Depósito')
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
    status = models.IntegerField('Situação', choices=STATUS_, default=0, blank=True)
    opcao_pagamento = models.CharField('Opção de pagamentos', choices=OPCAO_PAGAMENTO_, max_length=10, default='deposito')
    criado = models.DateTimeField('Criado em', auto_now_add=True)#é adicionado no momento da criação, não pode ser alterado
    modificado = models.DateTimeField('Modificado em', auto_now=True)#é adicionado no momento da modificação, pode ser alterado

    objects = GerenciadorPedido()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return 'Pedido {}'.format(self.pk)

    def produtos(self):
        produtos_ids = self.itens.values_list('produto')
        return Produto.objects.filter(pk__in=produtos_ids)

    def total(self):#metodo para somar os total dos preços do itens do carrinho
        aggregate_queryset = self.itens.aggregate(
            total=models.Sum(
                models.F('preco') * models.F('quantidade'),
                output_field=models.DecimalField()
            )
        )
        return aggregate_queryset['total']

    def pagseguro_update_status(self, status):
        if status == '3':
            self.status = 1
        elif status == '7':
            self.status = 2
        self.save()

    def pagseguro(self):
        pg = PagSeguro(#passa as informações da conta do pagseguro que estão no settings
            email=settings.PAGSEGURO_EMAIL,
            token=settings.PAGSEGURO_TOKEN,
            config={
                'sandbox':settings.PAGSEGURO_SANDBOX
            }
        )

        pg.sender = {#envia as informações de quem está fazendo a compra, olhar a documentação para ver quais campos é necessário
            'email':self.usuario.email
        }
        pg.reference_prefix = None #este campo serve para o pagseguro nos notificar quando houver notificaações no pagamento
        pg.shipping = None #dados da entrega
        pg.reference = self.pk #id do pedido
        
        for item in self.itens.all():
            pg.items.append(
                {
                    'id' : item.produto.pk,
                    'description' : item.produto.nome,
                    'quantity' : item.quantidade,
                    'amount' : '%.2f' % item.preco
                }
            )
        return pg

    def paypal(self):
        paypal_dict = {
            'upload' : '1',#se houver a possibilidade de haver mais de um item no carrinho, então é obrigatório usar essa variável
            'business' : settings.PAYPAL_EMAIL,
            'invoice' : self.pk,#referencia um id de um pedido do nosso sistema
            'cmd' : '_cart',#se houver a possibilidade de haver mais de um item no carrinho, então é obrigatório usar essa variável
            'currency_code' : 'BRL',
            'charset' : 'utf-8',
        }

        index=1
        for item in self.itens.all():#itens vem do atributo nomeado na classe ItensPedido
            paypal_dict['amount_{}'.format(index)] = '%.2f' % item.preco
            paypal_dict['item_name_{}'.format(index)] = item.produto.nome
            paypal_dict['quantity_{}'.format(index)] = item.quantidade
            index += 1
        return paypal_dict


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
 
