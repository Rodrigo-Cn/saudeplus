from django.shortcuts import render, redirect, get_object_or_404
from .forms import MedicamentoForm
from django.contrib import messages
from .models import Medicamento
from django.core.paginator import Paginator

def home(request):
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
            'resultado':resultado
        }
    else:
        context = {
            'form': form,
            'medicamentos':med_page,
        }

    return render(request, "medicamentos/medicamentos.html", context)

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
        
def detail(request, id):
    medicamento_detail = Medicamento.objects.get(pk=id)
    form = MedicamentoForm(instance=medicamento_detail)

    context = {'medicamento_detail': medicamento_detail, 'form' : form}
    return render(request, 'medicamentos/detail.html', context) 

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
