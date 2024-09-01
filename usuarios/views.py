from django.shortcuts import render
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm
from medicos.forms import MedicoCreationForm
from medicos.models import Medico
from pacientes.models import Paciente
from consultas.models import Consulta
from cids.models import Cid
from medicamentos.models import Medicamento
from django.core.paginator import Paginator

class CustomLoginView(auth_views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

def home(request):
    getter = request.GET.get('nome')
    dic = {}

    if getter:
        dic['nome__icontains'] = getter

    medicos = Medico.objects.filter(**dic)
    medico_count = Medico.objects.all()

    cids = Cid.objects.all()

    pacientes = Paciente.objects.count()
    consultas = Consulta.objects.count()
    medicamentos = Medicamento.objects.count() 

    medicos_paginator = Paginator(medicos, 8) 
    cids_paginator = Paginator(cids, 10)

    if request.GET.get('page'):
        page_num = request.GET.get('page')
    else:
        page_num = 1

    if request.GET.get('pagecid'):
        page_cid = request.GET.get('pagecid')
    else:
        page_cid = 1

    cid_page = cids_paginator.get_page(page_cid)
    med_page = medicos_paginator.get_page(page_num) 

    formdoctor = MedicoCreationForm()
    context = {
        'form': formdoctor,
        'medicos': med_page,
        'page': page_num,
        'page_cid':page_cid,
        'med_count': medico_count.count(),
        'pac_count': pacientes,
        'cons_count': consultas,
        'medicamento_count': medicamentos,
        'cids':cid_page,
    }
    
    return render(request, 'administrador/home.html', context)
