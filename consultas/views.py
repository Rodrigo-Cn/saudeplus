from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Consulta
from .forms import ConsultaCreationForm, ConsultaEditForm, Cons_medicamentoEditForm
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Cons_medicamento
from django.contrib.auth.decorators import login_required
from medicos.models import Medico
from django.contrib.auth.decorators import user_passes_test

def is_medico_ou_estudante(user):
    return user.groups.filter(name__in=['Medico', 'Estudante']).exists()

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def read(request):

    user = request.user
    medico = Medico.objects.get(pk=user.id)

    consultas = Consulta.objects.all()

    form = ConsultaCreationForm()
    context = {'consultas': consultas, 'form':form, 'medico':medico}
    return render(request, 'consultas/table.html', context)

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def add(request):

    user = request.user
    medico = Medico.objects.get(pk=user.id)

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
    return render(request, 'consultas/add.html', {'form': form, 'medico':medico})

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def remove(request, consulta_id):
    paciente = get_object_or_404(Consulta, id=consulta_id)
    paciente.delete()

    messages.info(request, 'Consulta deletada com sucesso')

    return redirect('read-consulta') 

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def edit(request, consulta_id):
    
    user = request.user
    medico = Medico.objects.get(pk=user.id)

    paciente = get_object_or_404(Consulta, pk=consulta_id)

    if request.method == 'POST':
        form = ConsultaEditForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta atualizada com sucesso!')
            return redirect('read-consulta')
    else:
        form = ConsultaEditForm(instance=paciente)
    return render(request, 'consultas/editConsulta.html', {'form':form, 'medico':medico})

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def detail(request, consulta_id):
    
    user = request.user
    medico = Medico.objects.get(pk=user.id)

    consulta = Consulta.objects.get(pk=consulta_id)
    form = ConsultaEditForm(instance=consulta)
    receitas = Cons_medicamento.objects.filter(consulta_id=consulta_id)
    context = {'consulta': consulta, 'form' : form, 'cids':consulta.cids.all(), 'medicamentos':consulta.medicamentos.all(), 'receitas':receitas, 'medico':medico}
    return render(request, 'consultas/detail.html', context) 

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def editar_receita(request, receita_id):
        
    user = request.user
    medico = Medico.objects.get(pk=user.id)

    receita = Cons_medicamento.objects.get(pk=receita_id)
    if request.method == 'POST':
        form = Cons_medicamentoEditForm(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            return redirect('read-consulta')
    else:
        form = Cons_medicamentoEditForm(instance=receita)
    return render(request, 'consultas/editReceita.html', {'form':form, 'medico':medico})