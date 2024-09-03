from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Medico
from .forms import MedicoCreationForm, MedicoEditForm, MedicoForm2
from django.contrib import messages
from .forms import MedicoEditForm
from django.contrib.auth.decorators import login_required
from medicos.models import Medico
from pacientes.models import Paciente
from consultas.models import Consulta
from cids.models import Cid
from medicamentos.models import Medicamento
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test

def isEstudante(user):
    return user.groups.filter(name='Estudante').exists()

def isMedico(user):
    return user.groups.filter(name='Medico').exists()

def isAdministrador(user):
    return user.groups.filter(name='Administrador').exists()

def is_medico_ou_estudante(user):
    return user.groups.filter(name__in=['Medico', 'Estudante']).exists()

@login_required
def home(request):
    user = request.user

    if isAdministrador(user):
        return redirect('home-adm')
    elif is_medico_ou_estudante(user):
        medico = Medico.objects.get(pk=user.id)
        medicos = Medico.objects.count()
        cids = Cid.objects.count()
        pacientes = Paciente.objects.count()
        consultas = Consulta.objects.count()
        medicamentos = Medicamento.objects.count()

        context = {
            'medico': medico,
            'num_cids': cids,
            'num_pacientes': pacientes,
            'num_consultas': consultas,
            'num_medicamentos': medicamentos,
            'num_medicos': medicos,
        }
        return render(request, 'medicos/home.html', context)
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('login')

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def read(request):
    user = request.user
    medico = Medico.objects.get(pk=user.id)
    if request.GET:
        
        dic = {}
        
        for key, val in request.GET.lists():
            dic.update({key + "__contains": val[0]})

        medicos = Medico.objects.all().filter(**dic)
    else:
        medicos = Medico.objects.all()

    context = {'medicos': medicos, 'medico': medico}
    return render(request, 'medicos/table.html', context)

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def detail2(request, medico_id):

    user = request.user
    medico = Medico.objects.get(pk=user.id)

    medico_detail = Medico.objects.get(pk=medico_id)
    form = MedicoEditForm(instance=medico_detail)

    context = {'medico_detail': medico_detail, 'form' : form, 'medico': medico}
    return render(request, 'medicos/detail2.html', context)

@login_required
@user_passes_test(isAdministrador, login_url='/')
def detail(request, medico_id):

    medico_detail = Medico.objects.get(pk=medico_id)
    form = MedicoEditForm(instance=medico_detail)

    context = {'medico_detail': medico_detail, 'form' : form}
    return render(request, 'medicos/detail.html', context) 

@login_required
@user_passes_test(isAdministrador, login_url='/')
def add(request):
    if request.method == 'POST':
        form = MedicoCreationForm(request.POST, request.FILES)
        grupo = request.POST.get('grupo')
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if grupo == 'estudante':
                group = Group.objects.get(id=3)
            else:
                group = Group.objects.get(id=2)
            user.groups.add(group)

            messages.success(request, "Médico cadastrado com sucesso")
            return redirect('home-adm')
        else:
            messages.error(request, "Erro no cadastro")
    else:
        form = MedicoCreationForm()
    
    return render(request, 'template_name.html', {'form': form})


@login_required
@user_passes_test(isAdministrador, login_url='/')
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

@login_required
@user_passes_test(isAdministrador, login_url='/')
def remove(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    medico.delete()

    messages.warning(request, 'Medico deletado com sucesso')

    return redirect('home-adm') 

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def perfil(request):

    user = request.user
    medico_detail = Medico.objects.get(pk=user.id)

    context = {'medico': medico_detail}
    return render(request, 'medicos/perfil.html', context)

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def editperfil(request):

    user = request.user
    medico = Medico.objects.get(pk=user.id)
    
    if request.method == 'POST':
        form = MedicoForm2(request.POST, request.FILES,  instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil editado com sucesso")
        else:
            messages.error(request, "Erro ao editar o perfil")
        return render(request, 'medicos/editperfil.html', {'form': form, 'medico': medico})
    else:
        form = MedicoForm2(instance=medico)

    return render(request, 'medicos/editperfil.html', {'form': form, 'medico': medico})

