import json
from django.http import JsonResponse
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo
from apps.cadastro.models import User_mobile
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def cadastrar_soltura(request):
    if request.method == 'POST':
        try:
            # Parseando os dados JSON do corpo da requisição
            data = json.loads(request.body)

            nome_lider = data.get('nome_lider', '')  
            telefone_lider = data.get('telefone_lider', '')  

            # Verificando se o telefone do líder foi fornecido e se o usuário existe
            try:
                user = User_mobile.objects.get(celular=telefone_lider) if telefone_lider else None
                if telefone_lider and not user:
                    return JsonResponse({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            except User_mobile.DoesNotExist:
                pass  # Se não houver telefone_lider, não faz nada

            motorista_nome = data.get('motorista')
            coletores_nomes = data.get('coletores', [])  
            veiculo_placa = data.get('veiculo')  
            frequencia = data.get('frequencia')
            setor = data.get('setor')
            
            hora_entrega_chave = data.get('hora_entrega_chave')  # Novo campo
            hora_entrega_saida_frota = data.get('hora_entrega_saida_frota')  # Novo campo
            
            # Verificando se todos os campos obrigatórios foram preenchidos
            if not all([motorista_nome, coletores_nomes, veiculo_placa, frequencia, setor]):
                return JsonResponse({'error': 'Campos obrigatórios faltando'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                # Buscando os objetos no banco de dados
                motorista = Colaborador.objects.get(nome=motorista_nome, funcao="Motorista", status="ATIVO")
                coletores = Colaborador.objects.filter(nome__in=coletores_nomes, funcao="Coletor", status="ATIVO")
                veiculo = Veiculo.objects.get(placa_veiculo=veiculo_placa, status="ATIVO")

                # Criando a soltura
                soltura = Soltura.objects.create(
                    motorista=motorista,
                    veiculo=veiculo, 
                    frequencia=frequencia,
                    setores=setor,
                    celular=user.celular if user else "",  # Celular é enviado se o usuário for encontrado
                    lider=nome_lider,  # Agora usamos o nome do líder diretamente
                    hora_entrega_chave=hora_entrega_chave,  
                    hora_entrega_saida_frota=hora_entrega_saida_frota  
                )

                # Limita a 3 coletores
                soltura.coletores.set(coletores[:3]) 

                # Retornando os dados da soltura criada
                return JsonResponse({
                    "motorista": soltura.motorista.nome,
                    "matricula_motorista": soltura.motorista.matricula,
                    "coletores": [coletor.nome for coletor in soltura.coletores.all()],
                    "placa_veiculo": soltura.veiculo.placa_veiculo,
                    "frequencia": soltura.frequencia,
                    "setores": soltura.setores,
                    "celular": soltura.celular,
                    "lider": soltura.lider,
                    "hora_entrega_chave": soltura.hora_entrega_chave,  
                    "hora_entrega_saida_frota": soltura.hora_entrega_saida_frota  
                }, status=status.HTTP_201_CREATED)

            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Motorista, Coletor ou Veículo não encontrado ou inativo'}, status=status.HTTP_404_NOT_FOUND)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de dados inválido'}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'error': 'Método HTTP não permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
