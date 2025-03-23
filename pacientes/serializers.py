from rest_framework.serializers import ModelSerializer
from .models import Paciente

class PacienteSerializer(ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'
        