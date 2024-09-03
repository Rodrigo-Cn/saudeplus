# forms.py
from django import forms
from .models import Consulta, Cons_medicamento
from django_select2 import forms as s2forms
from medicos.models import Medico
from pacientes.models import Paciente
from cids.models import Cid
from medicamentos.models import Medicamento

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
    medico = forms.ModelChoiceField(
            queryset=Medico.objects.all(),
            widget=MedicoWidget(attrs={'class': 'form-control'}),
            required=True
        )

    paciente = forms.ModelChoiceField(
            queryset=Paciente.objects.all(),
            widget=PacienteWidget(attrs={'class': 'form-control'}),
            required=True
        )

    cids = forms.ModelMultipleChoiceField(
            queryset=Cid.objects.all(),
            widget=CidWidget(attrs={'class': 'form-control'}),
            required=True
        )

    medicamentos = forms.ModelMultipleChoiceField(
            queryset=Medicamento.objects.all(),
            widget=MedicamentoWidget(attrs={'class': 'form-control'}),
            required=True
        )

    class Meta():
        model = Consulta
        fields = [
            'data', 'pressao', 'glicose', 'f_cardiaca', 'temperatura', 
            'sat_oxigenio', 'altura', 'observacoes', 'medico', 'paciente','cids', 'medicamentos'
        ]
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pressao': forms.TextInput(attrs={'class': 'form-control'}),
            'glicose': forms.NumberInput(attrs={'class': 'form-control'}),
            'f_cardiaca': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control'}),
            'sat_oxigenio': forms.NumberInput(attrs={'class': 'form-control'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ConsultaEditForm(forms.ModelForm):
     
    class Meta():
        model = Consulta
        fields = ['observacoes','data', 'altura']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control'}),

        }

class Cons_medicamentoCreationForm(forms.ModelForm):
     
     class Meta():
        model = Cons_medicamento
        fields =  ['medicamento','dose', 'periodicidade', 'tempo_de_uso_dias']
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-control'}),
            'dose': forms.TextInput(attrs={'class': 'form-control'}),
            'periodicidade': forms.TextInput(attrs={'class': 'form-control'}),
            'tempo_de_uso_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }

class Cons_medicamentoEditForm(forms.ModelForm):
     
     class Meta():
        model = Cons_medicamento
        fields =   ['dose', 'periodicidade', 'tempo_de_uso_dias']
        widgets = {
            'dose': forms.TextInput(attrs={'class': 'form-control'}),
            'periodicidade': forms.TextInput(attrs={'class': 'form-control'}),
            'tempo_de_uso_dias': forms.NumberInput(attrs={'class': 'form-control'}),
        }
