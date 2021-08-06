# Generated by Django 3.2.4 on 2021-08-05 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Um nome curto que será usado para identificar de forma única você na plataforma', max_length=50, unique=True, verbose_name='Apelido / Usuário'),
        ),
    ]