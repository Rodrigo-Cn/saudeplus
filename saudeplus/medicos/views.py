from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Medico
from .forms import MedicoCreationForm, MedicoEditForm

"""def home(request):
    user = request.user
    medico = get_object_or_404(Medico, pk=user.id)
    context = {'medico': medico, 'nome': medico.nome}
    return render(request, 'medicos/home.html', context)
"""
def home(request, medico_id): #VIEW TEMPORÁRIA APENAS PARA TESTES
    medico = Medico.objects.get(pk=medico_id)
    context = {'medico': medico, 'nome': medico.nome}
    return render(request, 'medicos/home.html', context)

def read(request):
    if request.GET:
        
        dic = {}
        
        for key, val in request.GET.lists():
            dic.update({key + "__contains": val[0]})

        medicos = Medico.objects.all().filter(**dic)
    else:
        medicos = Medico.objects.all()

    context = {'medicos': medicos}
    return render(request, 'medicos/table.html', context)

def detail(request, medico_id):
    medico_detail = Medico.objects.get(pk=medico_id)
    context = {'medico_detail': medico_detail}
    return render(request, 'medicos/detail.html', context) 



