from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from .models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo

@api_view(['GET', 'POST'])
def cadastrar_soltura(request):
    if request.method == 'POST':
        motorista_nome = request.data.get('motorista')
        coletores_nomes = request.data.get('coletores', [])  
        veiculo_placa = request.data.get('veiculo')  
        frequencia = request.data.get('frequencia')
        setor = request.data.get('setor')
        celular = request.data.get('celular', '') 
        lider = request.data.get('lider', '')  

        if not all([motorista_nome, coletores_nomes, veiculo_placa, frequencia, setor]):
            return Response({'error': 'Campos obrigatórios faltando'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            motorista = Colaborador.objects.get(nome=motorista_nome, funcao="Motorista", status="ATIVO")
            coletores = Colaborador.objects.filter(nome__in=coletores_nomes, funcao="Coletor", status="ATIVO")
            veiculo = Veiculo.objects.get(placa_veiculo=veiculo_placa, status="ATIVO")
            soltura = Soltura.objects.create(
                motorista=motorista,
                veiculo=veiculo, 
                frequencia=frequencia,
                setores=setor,
                celular=celular,
                lider=lider
            )
            soltura.coletores.set(coletores[:3])
            return Response({
                "motorista": soltura.motorista.nome,
                "matricula_motorista": soltura.motorista.matricula,
                "coletores": [coletor.nome for coletor in soltura.coletores.all()],
                "placa_veiculo": soltura.veiculo.placa_veiculo,
                "frequencia": soltura.frequencia,
                "setores": soltura.setores,
                "celular": soltura.celular,
                "lider": soltura.lider
            }, status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist:
            return Response({'error': 'Motorista, Coletor ou Veículo não encontrado ou inativo'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'GET':
        try:
            veiculos_ativos = Veiculo.objects.filter(status='ATIVO').values('placa_veiculo')
            motoristas = Colaborador.objects.filter(funcao='Motorista', status='ATIVO').values('nome', 'matricula')
            coletores = Colaborador.objects.filter(funcao='Coletor', status='ATIVO').values('nome')
            frequencias = ["Diária", "Semanal"]
            setores = ["Norte", "Sul", "Centro", "Oeste"]
            return Response({
                "veiculos": list(veiculos_ativos),
                "motoristas": list(motoristas),
                "coletores": list(coletores),
                "frequencias": frequencias,
                "setores": setores
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
