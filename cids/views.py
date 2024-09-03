from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Cid
from medicos.models import Medico
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

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


