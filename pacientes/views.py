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

@login_required
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
def add(request):
    if request.method == 'POST':
        form = PacienteCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            #user = form.save(commit=False)
            #user.save()
            #group = Group.objects.get(id=2)
            #user.groups.add(group)
    messages.info(request, 'Paciente adicionado com sucesso')
    return redirect('read-paciente')

@login_required
def remove(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    paciente.delete()

    messages.info(request, 'Paciente deletado com sucesso')

    return redirect('read-paciente') 

@login_required
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