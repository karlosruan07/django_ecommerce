
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db.models.fields import EmailField


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Apelido ou Usuário', max_length=50,
    unique=True, help_text='Um nome curto que será usado para identificar de forma única você na plataforma')
    name = models.CharField('Nome', max_length=100)
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField('Equipe', default=False)#verifica se o usuário é ou não membro da equipe
    is_active = models.BooleanField('Ativo', default=True)#com isso podemos ativar ou desativar o usuario em vez de apagar a conta dele    
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.name or self.username

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(" ")[0]
