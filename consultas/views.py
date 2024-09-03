from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Consulta
from .forms import ConsultaCreationForm, ConsultaEditForm, Cons_medicamentoEditForm
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Cons_medicamento

def read(request):

    consultas = Consulta.objects.all()

    form = ConsultaCreationForm()
    context = {'consultas': consultas, 'form':form}
    return render(request, 'consultas/table.html', context)

def add(request):
    if request.method == 'POST':
        form = ConsultaCreationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.save()  # Primeiro, salva o objeto principal para obter o ID
            form.save_m2m()
            
            messages.success(request, "Consulta adicionada com sucesso!")
            return redirect('read-consulta')
        else:
            messages.error(request, "Ocorreu um erro ao adicionar a consulta. Verifique os dados informados.")
    else:
        form = ConsultaCreationForm()
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
    return render(request, 'consultas/editConsulta.html', {'form':form})

def detail(request, consulta_id):

    consulta = Consulta.objects.get(pk=consulta_id)
    form = ConsultaEditForm(instance=consulta)
    receitas = Cons_medicamento.objects.filter(consulta_id=consulta_id)
    context = {'consulta': consulta, 'form' : form, 'cids':consulta.cids.all(), 'medicamentos':consulta.medicamentos.all(), 'receitas':receitas}
    return render(request, 'consultas/detail.html', context) 

def editar_receita(request, receita_id):
    receita = Cons_medicamento.objects.get(pk=receita_id)
    if request.method == 'POST':
        form = Cons_medicamentoEditForm(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            return redirect('read-consulta')
    else:
        form = Cons_medicamentoEditForm(instance=receita)
    return render(request, 'consultas/editReceita.html', {'form':form})