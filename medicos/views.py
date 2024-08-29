from django import template
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from .models import Medico

def home(request, medico_id):
    medico = Medico.objects.get(pk=medico_id)
    nome = medico.nome
    template = loader.get_template("medicos/home.html")
    context = {'medico':medico, 'nome':nome}
    return HttpResponse(template.render(context,request))