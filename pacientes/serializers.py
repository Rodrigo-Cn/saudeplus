from rest_framework import serializers  # Importando serializers
from rest_framework.serializers import ModelSerializer
from .models import Paciente

class PacienteSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Paciente
        fields = '__all__'

        