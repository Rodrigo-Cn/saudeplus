from django.db import models

class Cid(models.Model):
    codigo = models.CharField(max_length=4)
    nome = models.CharField(max_length=70)
    descricao = models.TextField()