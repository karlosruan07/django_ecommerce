from django.contrib import admin
from django.db.models.deletion import CASCADE

from .models import Carrinho

admin.site.register(Carrinho)

