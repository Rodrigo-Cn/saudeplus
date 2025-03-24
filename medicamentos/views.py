from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Medicamento
from .forms import MedicamentoForm
from .serializers import MedicamentoSerializer
from .paginations import MedicamentoPagination
from medicos.models import Medico

def is_medico_ou_estudante(user):
    return user.groups.filter(name__in=['Medico', 'Estudante']).exists()


@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def home(request):
    user = request.user
    medico_logado = Medico.objects.get(pk=user.id)
    query = request.GET.get('query') or request.GET.get('nome', '')
    dic = {}
    if query:
        dic['nome__icontains'] = query

    form = MedicamentoForm()
    medicamentos = Medicamento.objects.filter(**dic).order_by('nome')
    resultado = medicamentos.count()

    page_num = request.GET.get('page', 1)
    paginator = Paginator(medicamentos, 12)
    page = paginator.get_page(page_num)

    context = {
        'form': form,
        'medicamentos': page,
        'medico': medico_logado,
    }
    if query:
        context['resultado'] = resultado
        context['getter'] = query

    return render(request, "medicamentos/medicamentos.html", context)

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def add(request):

    if request.method == 'POST':
        form = MedicamentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Medicamento cadastrado com sucesso")
        else:
            messages.error(request, "Erro no cadastro")
        return redirect('home-medicamento')
    else:
        messages.error(request, "Método não permitido")
        return redirect('home-medicamento')

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def detail(request, id):
 
    user = request.user
    medico = Medico.objects.get(pk=user.id)
    medicamento_detail = Medicamento.objects.get(pk=id)
    form = MedicamentoForm(instance=medicamento_detail)

    context = {'medicamento_detail': medicamento_detail, 'form': form, 'medico': medico}
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
                messages.error(request, f"Erro ao editar {medicamento.nome}: {str(e)}")
        else:
            messages.error(request, "Erro ao editar. Verifique os campos e tente novamente.")
        return redirect('home-medicamento')
    else:
        messages.error(request, f"{medicamento.nome}: erro ao carregar o formulário de edição")
        return redirect('home-medicamento')

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def remove(request, id):
   
    medicamento = get_object_or_404(Medicamento, id=id)
    medicamento.delete()
    messages.warning(request, "Medicamento deletado com sucesso")
    return redirect('home-medicamento')

# ---- Endpoints da API (JSON) com JWT e Permissão IsAuthenticated ----

class MedicamentosList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        nome = request.query_params.get('nome')
        if nome:
            medicamentos = Medicamento.objects.filter(nome__icontains=nome)
        else:
            medicamentos = Medicamento.objects.all()
            
        paginator = MedicamentoPagination()
        page = paginator.paginate_queryset(medicamentos, request)

        if page is not None:
            serializer = MedicamentoSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(MedicamentoSerializer(medicamentos, many=True).data)
    
    def post(self, request):
        serializer = MedicamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Erro ao criar Medicamento.", "errors": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

class MedicamentoViewDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            medicamento = Medicamento.objects.get(pk=id)
        except Medicamento.DoesNotExist:
            return Response({"message": "Medicamento não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MedicamentoSerializer(medicamento)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            medicamento = Medicamento.objects.get(pk=id)
        except Medicamento.DoesNotExist:
            return Response({"message": "Medicamento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MedicamentoSerializer(medicamento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            medicamento = Medicamento.objects.get(pk=id)
        except Medicamento.DoesNotExist:
            return Response({"message": "Medicamento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        nome = medicamento.nome
        medicamento.delete()
        return Response({"message": f"Medicamento: {nome} deletado com sucesso."}, status=status.HTTP_200_OK)
