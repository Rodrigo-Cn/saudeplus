from django.shortcuts import render, get_object_or_404
from .models import Medico

def home(request):
    user = request.user
    medico = get_object_or_404(Medico, pk=user.id)
    context = {'medico': medico, 'nome': medico.nome}
    return render(request, 'medicos/home.html', context)
