
from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.CadastrarUsuario.as_view(), name='cadastrar'),
    path('conta/', views.IndexView.as_view(), name='conta'),
]

