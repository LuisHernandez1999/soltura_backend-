from rest_framework import serializers
from .models import User_mobile

class UserSerializer(serializers.ModelSerializer):
    senha_confirmar = serializers.CharField(write_only=True)  
    class Meta:
        model = User_mobile
        fields = ['nome', 'celular', 'senha', 'senha_confirmar']

def validate(self, data):
        senha = data.get('senha')
        senha_confirmar = data.pop('senha_confirmar', None)  

        if senha and senha_confirmar and senha != senha_confirmar:
            raise serializers.ValidationError({'senha': 'as senhas nao sao iguais.'})

        return data