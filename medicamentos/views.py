from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Medicamento
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
    query = request.GET.get('query', '')
    dic = Q()
    if query:
        dic |= Q(nome__icontains=query)
        
    medicamentos = Medicamento.objects.filter(dic).order_by('nome').distinct()
    resultado = medicamentos.count()

    page_num = request.GET.get('page', 1)
    paginator = Paginator(medicamentos, 12)
    page = paginator.get_page(page_num)

    context = {
        'medicamentos': page,
        'medico': medico_logado,
    }
    if query:
        context['resultado'] = resultado
        context['query'] = query

    return render(request, "medicamentos/medicamentos.html", context)

class MedicamentosList(APIView):

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
        return Response({"message": "Erro ao criar Medicamento."}, status=status.HTTP_400_BAD_REQUEST)

class MedicamentoViewDetail(APIView):

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
