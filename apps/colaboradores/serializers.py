from rest_framework import serializers
from .models import Colaboradores

class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaboradores
        fields = ['nome', 'matricula', 'pa', 'turno', 'tipo']