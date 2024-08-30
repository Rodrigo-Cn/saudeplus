# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

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
