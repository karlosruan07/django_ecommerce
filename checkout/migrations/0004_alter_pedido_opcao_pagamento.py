# Generated by Django 3.2.4 on 2021-09-02 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_itenspedido_pedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='opcao_pagamento',
            field=models.CharField(choices=[('pagseguro', 'PagSeguro'), ('paypal', 'Paypal'), ('deposito', 'Depósito')], default='deposito', max_length=10, verbose_name='Opção de pagamentos'),
        ),
    ]
