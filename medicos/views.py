from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Medico
from .forms import MedicoCreationForm, MedicoEditForm
from django.contrib import messages
from .forms import MedicoEditForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    user = request.user
    medico = Medico.objects.get(pk=user.id)
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
    form = MedicoEditForm(instance=medico_detail)

    context = {'medico_detail': medico_detail, 'form' : form}
    return render(request, 'medicos/detail.html', context) 

#TIRAR OS COMENTÁRIOS QUANDO OS GRUPOS ESTIVEREM PRONTOS
def add(request):
    if request.method == 'POST':
        form = MedicoCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            #user = form.save(commit=False)
            #user.save()
            #group = Group.objects.get(id=2)
            #user.groups.add(group)
        messages.success(request, "Médico cadastrado com sucesso")
        return redirect('home-adm')
    else:
        messages.error(request, "Erro no cadastro")
        return redirect('home-adm')
    
def edit(request, medico_id):
    medico = get_object_or_404(Medico, pk=medico_id)

    if request.method == 'POST':
        form = MedicoEditForm(request.POST, request.FILES, instance=medico)  # Inclua request.FILES para lidar com arquivos
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"CRM: {medico.crm} editado com sucesso")
            except Exception as e:
                messages.error(request, f"Erro ao editar CRM: {medico.crm}. Detalhes: {str(e)}")
        else:
            messages.error(request, "Erro ao editar. Verifique os campos e tente novamente.")
        return redirect('home-adm')
    else:
        messages.error(request, f"CRM: {medico.crm} erro ao carregar o formulário de edição")
        return redirect('home-adm')


def remove(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    medico.delete()

    messages.info(request, 'Medico deletado com sucesso')

    return redirect('home-adm') 