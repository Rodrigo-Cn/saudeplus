from django import forms
from .models import Medicamento

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            'foto_medicamento', 'nome', 'volume', 'apresentacao',
            'fabricante', 'composicao', 'posologia_recomendada', 'nome_substancia'
        ]
        labels = {
            'foto_medicamento': 'Foto do Medicamento',
            'nome': 'Nome',
            'volume': 'Volume',
            'apresentacao': 'Apresentação',
            'fabricante': 'Fabricante',
            'composicao': 'Composição',
            'posologia_recomendada': 'Posologia Recomendada',
            'nome_substancia': 'Nome da Substância',
        }
        widgets = {
            'foto_medicamento': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'aria-describedby': 'fotoMedicamentoHelp'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do Medicamento'
            }),
            'volume': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mg/ml'
            }),
            'apresentacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apresentação'
            }),
            'fabricante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fabricante'
            }),
            'composicao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Composição'
            }),
            'posologia_recomendada': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Posologia Recomendada'
            }),
            'nome_substancia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da Substância'
            }),
        }
