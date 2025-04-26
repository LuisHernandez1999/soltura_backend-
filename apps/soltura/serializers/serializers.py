from rest_framework import serializers
from ..models.models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo

class SolturaSerializer(serializers.ModelSerializer):
    motorista_nome = serializers.CharField(write_only=True)
    coletor_nome = serializers.CharField(write_only=True)
    veiculo_placa = serializers.CharField(write_only=True)
    motorista_nome_exibido = serializers.CharField(source='motorista.nome', read_only=True)
    coletor_nome_exibido = serializers.CharField(source='coletor.nome', read_only=True)
    veiculo_placa_exibida = serializers.CharField(source='veiculo.placa_veiculo', read_only=True)

    class Meta:
        model = Soltura
        fields = [
            'id', 'motorista', 'motorista_nome', 'motorista_nome_exibido', 
            'coletor', 'coletor_nome', 'coletor_nome_exibido', 'veiculo', 
            'veiculo_placa', 'veiculo_placa_exibida', 'hora_entrega_chave', 
            'hora_entrega_saida_frota', 'frequencia', 'setores', 'celular', 
            'lider', 'status'
        ]

    def validate(self, data):
        tipo_servico = data.get('tipo_servico')
        coletores = data.get('coletores', [])

        if tipo_servico == 'Varrição' and coletores:
            raise serializers.ValidationError("Varrição não deve ter coletores.")
        if tipo_servico != 'Varrição' and not coletores:
            raise serializers.ValidationError("É necessário informar coletores, exceto para Varrição.")
        return data

    def create(self, validated_data):
        motorista_nome = validated_data['motorista_nome']
        coletor_nome = validated_data['coletor_nome']
        veiculo_placa = validated_data['veiculo_placa']
        motorista = Colaborador.objects.get(nome=motorista_nome, funcao="Motorista", status="ATIVO")
        coletor = Colaborador.objects.get(nome=coletor_nome, funcao="Coletor", status="ATIVO")
        veiculo = Veiculo.objects.get(placa_veiculo=veiculo_placa, status="ATIVO")
        soltura = Soltura.objects.create(
            motorista=motorista,
            coletor=coletor,
            veiculo=veiculo,
            **validated_data
        )
        return soltura

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
