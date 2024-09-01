from django import forms
from usuarios.forms import UserCreationForm, UserChangeForm
from .models import Medico

class MedicoCreationForm(UserCreationForm):
    class Meta:
        model = Medico
        fields = [
            'foto_perfil', 'username', 'nome', 'crm', 'especialidade', 
            'telefone', 'hospital_clinica', 'data_nascimento'
        ]

        labels = {
            'hospital_clinica': 'Hospital ou Clínica',
        }

        widgets = {
            'foto_perfil': forms.ClearableFileInput(attrs={
                'class': 'form-control-file', 
                'aria-describedby': 'fotoPerfilHelp'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Usuário para login'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome Completo'
            }),
            'crm': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'CRM'
            }),
            'especialidade': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Especialidade'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Telefone'
            }),
            'hospital_clinica': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Hospital/Clínica'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Data de Nascimento', 
                'type': 'date'
            }),
        }

class MedicoEditForm(UserChangeForm):
    
    password = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Medico
        fields = ['foto_perfil', 'nome', 'crm', 'especialidade', 'telefone', 'hospital_clinica']

        widgets = {
            'foto_perfil': forms.ClearableFileInput(attrs={
                'class': 'form-control-file', 
                'aria-describedby': 'fotoPerfilHelp'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome Completo'
            }),
            'crm': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'CRM'
            }),
            'especialidade': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Especialidade'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Telefone'
            }),
            'hospital_clinica': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Hospital/Clínica'
            }),
        }

