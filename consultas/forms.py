# forms.py
from django import forms
from .models import Consulta, Cons_medicamento
from django_select2 import forms as s2forms
from medicos.models import Medico

class MedicoWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "nome__icontains",
        "crm__icontains",
        "telefone__icontains",
        "especialidade__icontains"
    ]


class PacienteWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "cpf__icontains",
    ]

class CidWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "codigo__icontains",
        "descricao__icontains",
    ]

class MedicamentoWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "nome__icontains",
        "fabricante__icontains",
        "nome_substancia__icontains",
        "fabricante__icontains"
    ]

class ConsultaCreationForm(forms.ModelForm):
   
    class Meta():
        model = Consulta
        fields =  '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pressao': forms.TextInput(attrs={'class': 'form-control'}),
            'glicose': forms.NumberInput(attrs={'class': 'form-control'}),
            'f_cardiaca': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control'}),
            'sat_oxigenio': forms.NumberInput(attrs={'class': 'form-control'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
            'medico': MedicoWidget(attrs={'class': 'form-control'}),
            'paciente': PacienteWidget(attrs={'class': 'form-control'}),
            'cids': CidWidget(attrs={'class': 'form-control'}),
            'medicamentos': MedicamentoWidget(attrs={'class': 'form-control'}),
        }


class ConsultaEditForm(forms.ModelForm):
     
    class Meta():
        model = Consulta
        fields = '__all__'
        widgets = {

        }

class Cons_medicamentoCreationForm(forms.ModelForm):
     
     class Meta():
        model = Cons_medicamento
        fields =  '__all__'
        widgets = {
 
        }

class Cons_medicamentoEditForm(forms.ModelForm):
     
     class Meta():
        model = Cons_medicamento
        fields =  '__all__'
        widgets = {
 
        }
