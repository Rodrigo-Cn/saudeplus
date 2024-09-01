from django.db import models
from medicos.models import Medico
from pacientes.models import Paciente
from cids.models import Cid
from medicamentos.models import Medicamento

class Consulta(models.Model):
    data = models.DateTimeField()
    pressao = models.CharField(max_length=7)
    glicose = models.DecimalField(max_digits=5, decimal_places=2)
    f_cardiaca = models.IntegerField()
    temperatura = models.DecimalField(max_digits=4, decimal_places=1)
    sat_oxigenio = models.DecimalField(max_digits=4, decimal_places=1)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    observacoes = models.TextField()
    medico = models.ForeignKey(Medico,on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    cids = models.ManyToManyField(Cid)
    medicamentos = models.ManyToManyField(Medicamento, through='Cons_medicamento')

    def __str__(self):
        return f"Consulta em {self.data} de {self.paciente.nome}"

class Cons_medicamento(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    medicamento = models.ForeignKey('medicamentos.Medicamento', on_delete=models.CASCADE)
    dose = models.CharField(max_length=20)
    periodicidade = models.CharField(max_length=40)
    tempo_de_uso_dias = models.IntegerField()