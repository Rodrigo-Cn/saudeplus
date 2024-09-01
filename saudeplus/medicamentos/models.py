from django.db import models

class Medicamento(models.Model):
    foto_medicamento = models.ImageField(upload_to='images/medicamentos/', height_field=None, width_field=None, max_length=255, blank=True)
    nome = models.CharField(max_length=100)
    volume = models.CharField(max_length=50, blank=True)
    apresentacao = models.CharField(max_length=50)
    fabricante = models.CharField(max_length=50)
    composicao = models.CharField(max_length=50)
    posologia_recomendada = models.CharField(max_length=50)
    nome_substancia = models.CharField(max_length=50)
