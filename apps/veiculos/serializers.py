from rest_framework import serializers
from .models import Veiculo

class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = ['prefixo', 'tipo',  'placa_veiculo', 'em_manutencao']