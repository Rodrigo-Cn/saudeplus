from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Paciente
from .forms import PacienteCreationForm, PacienteEditForm
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Paciente
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from medicos.models import Medico
from django.contrib.auth.decorators import user_passes_test
from consultas.models import Consulta

def is_medico_ou_estudante(user):
    return user.groups.filter(name__in=['Medico', 'Estudante']).exists()


def isAdministrador(user):
    return user.groups.filter(name='Administrador').exists()

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def read(request):

    user = request.user
    medico = Medico.objects.get(pk=user.id)

    if request.GET:
        
        dic = {}
        
        for key, val in request.GET.lists():
            dic.update({key + "__contains": val[0]})

        pacientes = Paciente.objects.all().filter(**dic)
    else:
        pacientes = Paciente.objects.all()

    formCreation = PacienteCreationForm()
    context = {'pacientes': pacientes, 'formCreation':formCreation, 'medico':medico}
    return render(request, 'pacientes/table.html', context)

@login_required
@user_passes_test(isAdministrador, login_url='/')
def adm(request):
    getter = request.GET.get('cpf')
    dic = {}

    if getter:
        dic['cpf__icontains'] = getter

    pacientes = Paciente.objects.filter(**dic).order_by('cpf')

    if request.GET.get('page'):
        page_num = request.GET.get('page')
    else:
        page_num = 1

    pacientes_paginator = Paginator(pacientes,15)

    pacientes_page = pacientes_paginator.get_page(page_num)

    context = {'pacientes': pacientes_page}
    return render(request, 'pacientes/table2.html', context)

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def add(request):
    if request.method == 'POST':
        form = PacienteCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            group = Group.objects.get(id=4)
            user.groups.add(group)
            messages.info(request, 'Paciente adicionado com sucesso')
        else:
            messages.error(request, 'Erro ao adicionar paciente')
    return redirect('read-paciente')

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def remove(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    paciente.delete()

    messages.info(request, 'Paciente deletado com sucesso')

    return redirect('read-paciente') 

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def edit(request, paciente_id):

    user = request.user
    medico = Medico.objects.get(pk=user.id)

    paciente = get_object_or_404(Paciente, pk=paciente_id)

    if request.method == 'POST':
        form = PacienteEditForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente atualizado com sucesso!')
            return redirect('read-paciente')
    else:
        form = PacienteEditForm(instance=paciente)
    return render(request, 'pacientes/edit.html', {'form':form, 'medico':medico})

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def registro(request, paciente_id):
    consultas = Consulta.objects.filter(paciente_id=paciente_id)  
    if not consultas.exists(): 
        messages.warning(request, 'Esse paciente não possui consultas!')
        return redirect('read-paciente')
    medico = Medico.objects.get(pk=request.user.id)
    return render(request, 'pacientes/view.html', {'consultas':consultas, 'medico':medico})
