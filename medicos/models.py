from django.db import models
from usuarios.models import Usuario

class Medico(Usuario):
    foto_perfil = models.ImageField(upload_to='images/medicos/', height_field=None, width_field=None, max_length=255, blank=True)
    nome = models.CharField(max_length=100)
    crm= models.CharField(max_length=10)
    especialidade= models.CharField(max_length=50)
    telefone= models.CharField(max_length=50, blank=True, null=True)
    hospital_clinica= models.CharField(max_length=100, blank=True, null=True)
