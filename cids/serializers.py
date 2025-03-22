from rest_framework.serializers import ModelSerializer
from .models import Cid

class CidSerializer(ModelSerializer):
    class Meta:
        model = Cid
        fields = '__all__'