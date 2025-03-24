from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Medico
from .forms import MedicoCreationForm, MedicoEditForm, MedicoForm2
from .serializers import MedicoSerializer
from .paginations import MedicoPagination

from cids.models import Cid
from pacientes.models import Paciente
from consultas.models import Consulta
from medicamentos.models import Medicamento

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
        medico_logado = Medico.objects.get(pk=user.id)
        query = request.GET.get('query', '')
        dic = Q()
        if query:
            dic |= Q(nome__icontains=query) | Q(crm__icontains=query) | Q(especialidade__icontains=query)
        medicos = Medico.objects.filter(dic).order_by('nome').distinct()
        resultado = medicos.count()
        page_num = request.GET.get('page', 1)
        medico_paginator = Paginator(medicos, 12)
        med_page = medico_paginator.get_page(page_num)
        context = {
            'medicos': med_page,
            'medico': medico_logado,
        }
        if query:
            context['resultado'] = resultado
            context['query'] = query
        return render(request, "medicos/medicos.html", context)
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('login')

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def read(request):

    user = request.user
    medico_logado = Medico.objects.get(pk=user.id)
    getter = request.GET.get('nome')
    dic = {}
    if getter:
        dic['nome__icontains'] = getter
    medicos = Medico.objects.filter(**dic).order_by('nome')
    resultado = medicos.count()
    page_num = request.GET.get('page', 1)
    medico_paginator = Paginator(medicos, 12)
    med_page = medico_paginator.get_page(page_num)
    context = {
        'medicos': med_page,
        'medico': medico_logado
    }
    if getter:
        context['resultado'] = resultado
        context['getter'] = getter
    return render(request, "medicos/table.html", context)

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def detail2(request, medico_id):
  
    user = request.user
    medico_logado = Medico.objects.get(pk=user.id)
    medico_detail = get_object_or_404(Medico, pk=medico_id)
    form = MedicoEditForm(instance=medico_detail)
    context = {'medico_detail': medico_detail, 'form': form, 'medico': medico_logado}
    return render(request, 'medicos/detail2.html', context)

@login_required
@user_passes_test(isAdministrador, login_url='/')
def detail(request, medico_id):
   
    medico_detail = get_object_or_404(Medico, pk=medico_id)
    form = MedicoEditForm(instance=medico_detail)
    context = {'medico_detail': medico_detail, 'form': form}
    return render(request, 'medicos/detail.html', context)

@login_required
@user_passes_test(isAdministrador, login_url='/')
def add(request):

    if request.method == 'POST':
        form = MedicoCreationForm(request.POST, request.FILES)
        grupo = request.POST.get('grupo')
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.save()
            if grupo == 'estudante':
                group = Group.objects.get(id=3)
            else:
                group = Group.objects.get(id=2)
            user_obj.groups.add(group)
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
        form = MedicoEditForm(request.POST, request.FILES, instance=medico)
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
  
    medico = get_object_or_404(Medico, pk=medico_id)
    medico.delete()
    messages.warning(request, 'Médico deletado com sucesso')
    return redirect('home-adm')

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def perfil(request):

    user = request.user
    medico_logado = get_object_or_404(Medico, pk=user.id)
    context = {'medico': medico_logado}
    return render(request, 'medicos/perfil.html', context)

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def editperfil(request):
 
    user = request.user
    medico_logado = get_object_or_404(Medico, pk=user.id)
    if request.method == 'POST':
        form = MedicoForm2(request.POST, request.FILES, instance=medico_logado)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil editado com sucesso")
        else:
            messages.error(request, "Erro ao editar o perfil")
        return render(request, 'medicos/editperfil.html', {'form': form, 'medico': medico_logado})
    else:
        form = MedicoForm2(instance=medico_logado)
    return render(request, 'medicos/editperfil.html', {'form': form, 'medico': medico_logado})

# ---- ENDPOINTS DA API (JSON) COM JWT ----

class MedicosList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        nome = request.query_params.get('nome')
        if nome:
            medicos = Medico.objects.filter(nome__icontains=nome)
        else:
            medicos = Medico.objects.all()
        paginator = MedicoPagination()
        page = paginator.paginate_queryset(medicos, request)
        if page is not None:
            serializer = MedicoSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response(MedicoSerializer(medicos, many=True).data)

    def post(self, request):
        serializer = MedicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Erro ao criar Médico.", "errors": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

class MedicoViewDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            medico = Medico.objects.get(pk=id)
        except Medico.DoesNotExist:
            return Response({"message": "Médico não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = MedicoSerializer(medico)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            medico = Medico.objects.get(pk=id)
        except Medico.DoesNotExist:
            return Response({"message": "Médico não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = MedicoSerializer(medico, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            medico = Medico.objects.get(pk=id)
        except Medico.DoesNotExist:
            return Response({"message": "Médico não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        nome = medico.nome
        medico.delete()
        return Response({"message": f"Médico: {nome} deletado com sucesso."}, status=status.HTTP_200_OK)
