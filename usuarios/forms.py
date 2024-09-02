from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'id': 'exampleInputEmail',
            'aria-describedby': 'emailHelp',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-user',
            'id': 'exampleInputPassword',
            'placeholder': 'Password'
        })
    )

class UsuarioCreationForm(UserCreationForm):
     
    class Meta():
        model = Usuario
        fields =  ['data_nascimento']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control form-control-user', 'type': 'date'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control form-control-user'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control form-control-user'}),
        }


class UsuarioEditForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ['data_nascimento']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
