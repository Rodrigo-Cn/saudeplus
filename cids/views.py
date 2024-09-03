from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Cid
from medicos.models import Medico
from django.contrib.auth.decorators import login_required

@login_required
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

    context = {
        'cids': cid_page,
        'resultado': resultado,
        'medico':medico,
        'query': query,
    }

    return render(request, "cids/cids.html", context)


