from django.db import models

class Cid(models.Model):
    codigo = models.CharField(max_length=4)
    descricao = models.TextField()

    def __str__(self):
        return self.descricao