from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Cid

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Cid

def home(request):
    query = request.GET.get('query', '')
    dic = {}

    if query:
        dic['descricao__icontains'] = query
        dic['codigo__icontains'] = query

    cids = Cid.objects.filter(**dic).order_by('descricao').distinct()

    resultado = cids.count()

    # Paginação
    page_num = request.GET.get('page', 1)
    cid_paginator = Paginator(cids, 1)
    cid_page = cid_paginator.get_page(page_num)

    context = {
        'cids': cid_page,
        'resultado': resultado,
        'query': query,
    }

    return render(request, "cids/cids.html", context)

