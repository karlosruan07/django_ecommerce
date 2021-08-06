from django.db import models

class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=100)#o primeiro parâmetro é o verbose nome
    slug = models.SlugField('Identificador', max_length=100)
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    modificado = models.DateTimeField('Modificado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']#pode ser ordenado em ordem alfabética, crescente, decrescente...

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Identificador', max_length=100)
    
    categoria = models.ForeignKey('catalog.Categoria', verbose_name='Categoria', on_delete=models.PROTECT)
    descricao = models.TextField('Descrição', blank=True) 
    preco = models.DecimalField('Preço', decimal_places=2, max_digits=8)# EX: 99999999, 99
    
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    modificado = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Produtos'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']
        
    def __str__(self):
        return self.nome
        
        