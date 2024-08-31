from django import forms
from usuarios.forms import UserCreationForm, UserChangeForm
from .models import Medico

class MedicoCreationForm(UserCreationForm):
     
    class Meta():
        model = Medico
        fields = ['foto_perfil', 'nome', 'crm', 'especialidade', 'telefone', 'hospital_clinica', 'data_nascimento']
        widgets = {
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control form-control-user'}),
            'nome': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'crm': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'especialidade': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'hospital_clinica': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }


class MedicoEditForm(UserChangeForm):
    
    class Meta():
        model = Medico
        fields = ['foto_perfil', 'nome', 'crm', 'especialidade', 'telefone', 'hospital_clinica']
        widgets = {

        }
