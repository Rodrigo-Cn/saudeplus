from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Medico
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MedicoSerializer
from .paginations import MedicoPagination

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

class MedicosList(APIView):

    def get(self, request):
        nome = request.query_params.get('nome')
        if nome:
            medicos = Medico.objects.filter(nome__icontains=nome)
        else:
            medicos = Medico.objects.all()
            
        paginator = MedicoPagination()
        page = paginator.paginate_queryset(medicos, request)

        if page is not None:
            medico_serializer = MedicoSerializer(page, many=True)
            return paginator.get_paginated_response(medico_serializer.data)

        return Response(MedicoSerializer(medicos, many=True).data)
    
    def post(self, request):
        medico_serializer = MedicoSerializer(data=request.data)
        if medico_serializer.is_valid():
            medico_serializer.save()
            return Response(medico_serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Erro ao criar Médico."}, status=status.HTTP_400_BAD_REQUEST)

class MedicoViewDetail(APIView):
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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            medico = Medico.objects.get(pk=id)
        except Medico.DoesNotExist:
            return Response({"message": "Médico não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        nome = medico.nome
        medico.delete()
        return Response({"message": f"Médico: {nome} deletado com sucesso."}, status=status.HTTP_200_OK)
