from django.db import models
from django.contrib.auth.models import User

class Usuario(User):

    data_nascimento = models.DateField()

    def __str__(self):
        return self.username
