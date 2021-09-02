
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.db.models import fields
from django import forms
from .models import User

class FormularioAdmin(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email']#a senha e a confirmação de senha, o UserCreationForm já trata disso

class FormularioAdminUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'is_active', 'is_staff']

