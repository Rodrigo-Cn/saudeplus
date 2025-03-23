from rest_framework.serializers import ModelSerializer
from .models import Medicamento

class MedicamentoSerializer(ModelSerializer):
    class Meta:
        model = Medicamento
        fields = '__all__'