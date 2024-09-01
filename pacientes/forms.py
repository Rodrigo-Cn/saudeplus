# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import Paciente
from django.contrib.auth import password_validation

class PacienteCreationForm(UserCreationForm):

    password1 = forms.CharField(
        label=("Senha"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control form-control-user'}),
        help_text=password_validation.password_validators_help_text_html(),

    )
    password2 = forms.CharField(
        label=("Confirme sua senha"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control form-control-user'}),
        strip=False,
        help_text=("Insira a mesma senha que a anterior, para verificação."),

    )
     
    class Meta():
        model = Paciente
        fields =  ['data_nascimento', 'cpf', 'sexo', 'username']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control form-control-user', 'type': 'date'}),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                'maxlength': '11',
                'title': 'Digite um CPF válido com 11 dígitos',
                'placeholder': 'Digite o CPF'
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-control form-control-user',
            }),
            'data_nascimento': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'username': forms.TextInput(attrs={'class': 'form-control form-control-user'})
        }


class PacienteEditForm(UserChangeForm):
    password = None
     
    class Meta():
        model = Paciente
        fields = ['data_nascimento', 'cpf', 'sexo']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control form-control-user', 'type': 'date'}),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                'maxlength': '11',
                'title': 'Digite um CPF válido com 11 dígitos',
                'placeholder': 'Digite o CPF'
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-control form-control-user',
            }),
            'data_nascimento': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }
