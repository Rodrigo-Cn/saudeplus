from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Consulta
from .forms import ConsultaCreationForm, ConsultaEditForm
from django.contrib.auth.models import Group
from django.contrib import messages


def read(request):
    if request.GET:
        
        dic = {}
        
        for key, val in request.GET.lists():
            dic.update({key + "__contains": val[0]})

        consultas = Consulta.objects.all().filter(**dic)
    else:
        consultas = Consulta.objects.all()

    form = ConsultaCreationForm()
    context = {'consultas': consultas, 'form':form}
    return render(request, 'consultas/table.html', context)

def add(request):
    if request.method == 'POST':
        form = ConsultaCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Consulta adicionada!")
            return redirect('read-consulta')
    else:
        form = ConsultaCreationForm()  # Instanciando o formulário corretamente

    return render(request, 'consultas/add.html', {'form': form})


def remove(request, consulta_id):
    paciente = get_object_or_404(Consulta, id=consulta_id)
    paciente.delete()

    messages.info(request, 'Consulta deletada com sucesso')

    return redirect('read-consulta') 

def edit(request, consulta_id):
    paciente = get_object_or_404(Consulta, pk=consulta_id)

    if request.method == 'POST':
        form = ConsultaEditForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta atualizada com sucesso!')
            return redirect('read-consulta')
    else:
        form = ConsultaEditForm(instance=paciente)
    return render(request, 'consultas/edit.html', {'form':form})

def detail(request, consulta_id):

    consulta_detail = Consulta.objects.get(pk=consulta_id)
    form = ConsultaEditForm(instance=consulta_detail)

    context = {'consulta_detail': consulta_detail, 'form' : form}
    return render(request, 'consultas/detail.html', context) 
