from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Cid
from medicos.models import Medico
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CidSerializer
from .paginations import CidPagination
from rest_framework import status

def is_medico_ou_estudante(user):
    return user.groups.filter(name__in=['Medico', 'Estudante']).exists()

@login_required
@user_passes_test(is_medico_ou_estudante, login_url='/')
def home(request):
    user = request.user
    medico = Medico.objects.get(pk=user.id)
    query = request.GET.get('query', '')
    dic = Q()

    if query:
        dic |= Q(descricao__icontains=query) | Q(codigo__icontains=query)

    cids = Cid.objects.filter(dic).order_by('descricao').distinct()

    resultado = cids.count()

    page_num = request.GET.get('page', 1)
    cid_paginator = Paginator(cids, 12)
    cid_page = cid_paginator.get_page(page_num)

    if query:
        context = {
            'cids': cid_page,
            'resultado': resultado,
            'medico':medico,
            'query': query,
        }
    else:
        context = {
            'cids': cid_page,
            'medico':medico,
            'query': query,
        }

    return render(request, "cids/cids.html", context)

class CidsList(APIView):

    def get(self, request):
        codigo = request.query_params.get('codigo')
        if codigo:
            cids = Cid.objects.filter(codigo__icontains=codigo)
        else:
            cids = Cid.objects.all()
            
        paginator = CidPagination()
        page = paginator.paginate_queryset(cids, request)

        if page is not None:
            cids_serializer = CidSerializer(page, many=True)
            return paginator.get_paginated_response(cids_serializer.data)

        return Response(CidSerializer(cids, many=True).data)
    
    def post(self, request):
        cid_serializer = CidSerializer(data=request.data)
        if cid_serializer.is_valid():
            cid_serializer.save()
            return Response(cid_serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Erro ao criar CID."}, status=status.HTTP_400_BAD_REQUEST)


