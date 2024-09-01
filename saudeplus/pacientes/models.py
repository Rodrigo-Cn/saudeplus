from django.db import models
from usuarios.models import Usuario

class Paciente(Usuario):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    cpf = models.CharField(max_length=11)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    def __str__(self):
        return self.usuario.username