
from django.urls import path
from . import views

from django.contrib.auth import views as authview

urlpatterns = [

    path('cadastrar/', views.CadastrarUsuario.as_view(), name='cadastrar'),
    path('editar-dados/', views.EditarDadosUsuario.as_view(), name='editar-dados-usuario'),

    #URLs de autenticação
    path('alterar-senha/', authview.PasswordChangeView.as_view(template_name='accounts/alterar_senha.html'), name='alterar-senha'),
    path('senha-alterada/', authview.PasswordChangeDoneView.as_view(template_name='accounts/senha_alterada.html'), name='senha-alterada'),
    path('resetar-senha/', authview.PasswordResetView.as_view(template_name='accounts/resetar_senha.html'), name='resetar-senha'),

]

