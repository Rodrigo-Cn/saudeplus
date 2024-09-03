from django import forms
from usuarios.forms import UserCreationForm, UserChangeForm, UsuarioEditForm
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

class MedicoForm2(UsuarioEditForm):
    class Meta:
        model = Medico
        fields = ['username', 'nome', 'crm', 'especialidade', 'telefone', 'hospital_clinica', 'data_nascimento','foto_perfil']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'inputUsername',
                'placeholder': 'Digite seu usuário'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'inputNome',
                'placeholder': 'Digite seu nome'
            }),
            'crm': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'inputCRM',
                'placeholder': 'Digite seu CRM'
            }),
            'especialidade': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'inputEspecialidade',
                'placeholder': 'Digite sua especialidade'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'inputTelefone',
                'placeholder': 'Digite seu telefone'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'inputDataNascimento',
            }),
            'hospital_clinica': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'inputHospitalClinica',
                'placeholder': 'Digite o nome do hospital/clínica'
            }),
            'foto_perfil': forms.ClearableFileInput(attrs={
                'class': 'form-control-file', 
                'aria-describedby': 'fotoPerfilHelp'
            }),
        }


