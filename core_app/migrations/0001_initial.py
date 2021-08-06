# Generated by Django 3.2.4 on 2021-06-29 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('email', models.EmailField(max_length=50, verbose_name='Email')),
                ('titulo', models.CharField(max_length=255, verbose_name='Titulo')),
                ('mensagem', models.TextField(verbose_name='Mensagem')),
            ],
        ),
    ]
