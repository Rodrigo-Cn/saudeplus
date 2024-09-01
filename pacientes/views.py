from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Paciente
from .forms import PacienteCreationForm, PacienteEditForm
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Paciente

def read(request):
    if request.GET:
        
        dic = {}
        
        for key, val in request.GET.lists():
            dic.update({key + "__contains": val[0]})

        pacientes = Paciente.objects.all().filter(**dic)
    else:
        pacientes = Paciente.objects.all()

    formCreation = PacienteCreationForm()
    context = {'pacientes': pacientes, 'formCreation':formCreation}
    return render(request, 'pacientes/table.html', context)

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


def remove(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    paciente.delete()

    messages.info(request, 'Paciente deletado com sucesso')

    return redirect('read-paciente') 

def edit(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)

    if request.method == 'POST':
        form = PacienteEditForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente atualizado com sucesso!')
            return redirect('read-paciente')
    else:
        form = PacienteEditForm(instance=paciente)
    return render(request, 'pacientes/edit.html', {'form':form})