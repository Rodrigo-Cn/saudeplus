from django.shortcuts import render, redirect, get_object_or_404
from .forms import MedicamentoForm
from django.contrib import messages
from .models import Medicamento
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from medicos.models import Medico
from django.contrib.auth.decorators import user_passes_test

def is_medico_ou_estudante(user):
    return user.groups.filter(name__in=['Medico', 'Estudante']).exists()

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def home(request):

    user = request.user
    medico = Medico.objects.get(pk=user.id)

    getter = request.GET.get('nome')
    dic = {}

    if getter:
        dic['nome__icontains'] = getter

    form = MedicamentoForm()

    medicamentos = Medicamento.objects.filter(**dic).order_by('nome')

    resultado = Medicamento.objects.filter(**dic).order_by('nome').count()

    if request.GET.get('page'):
        page_num = request.GET.get('page')
    else:
        page_num = 1

    medicamentos_paginator = Paginator(medicamentos,12)

    med_page = medicamentos_paginator.get_page(page_num)

    if getter:
        context = {
            'form': form,
            'medicamentos':med_page,
            'resultado':resultado,
            'getter':getter,
            'medico':medico
        }
    else:
        context = {
            'form': form,
            'medicamentos':med_page,
            'medico':medico
        }

    return render(request, "medicamentos/medicamentos.html", context)

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def add(request):
        if request.method == 'POST':
            form = MedicamentoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(commit=True)
            messages.success(request, "Médicamento cadastrado com sucesso")
            return redirect('home-medicamento')
        else:
            messages.error(request, "Erro no cadastro")
            return redirect('home-medicamento')

@login_required 
@user_passes_test(is_medico_ou_estudante, login_url='/')
def detail(request, id):

    user = request.user
    medico = Medico.objects.get(pk=user.id)

    medicamento_detail = Medicamento.objects.get(pk=id)
    form = MedicamentoForm(instance=medicamento_detail)

    context = {'medicamento_detail': medicamento_detail, 'form' : form, 'medico':medico}
    return render(request, 'medicamentos/detail.html', context) 

@login_required 
@user_passes_test(is_medico_ou_estudante, login_url='/')
def edit(request, id):
    medicamento = get_object_or_404(Medicamento, pk=id)

    if request.method == 'POST':
        form = MedicamentoForm(request.POST, request.FILES, instance=medicamento)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"{medicamento.nome} editado(a) com sucesso")
            except Exception as e:
                messages.error(request, f"Erro ao editar o {medicamento.nome}. Detalhes: {str(e)}")
        else:
            messages.error(request, "Erro ao editar. Verifique os campos e tente novamente.")
        return redirect('home-medicamento')
    else:
        messages.error(request, f"{medicamento.nome} erro ao carregar o formulário de edição")
        return redirect('home-medicamento')

@login_required 
@user_passes_test(is_medico_ou_estudante, login_url='/')
def remove(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    medicamento.delete()

    messages.warning(request, 'Medicamento deletado com sucesso')

    return redirect('home-medicamento') 
