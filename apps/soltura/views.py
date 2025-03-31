import json
from django.http import JsonResponse
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo
from apps.cadastro.models import User_mobile
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

@csrf_exempt
def cadastrar_soltura(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Dados recebidos: {data}") 
            
            nome_lider = data.get('nome_lider', '')
            telefone_lider = data.get('telefone_lider', '')

            try:
                user = User_mobile.objects.get(celular=telefone_lider) if telefone_lider else None
                if telefone_lider and not user:
                    return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
            except User_mobile.DoesNotExist:
                pass

            motorista_nome = data.get('motorista')
            coletores_nomes = data.get('coletores', [])
            veiculo_placa = data.get('veiculo')
            frequencia = data.get('frequencia')
            setor = data.get('setor')
            hora_entrega_chave = data.get('hora_entrega_chave')
            hora_entrega_saida_frota = data.get('hora_entrega_saida_frota')

            # Verificando se todos os campos obrigatórios foram preenchidos
            if not all([motorista_nome, coletores_nomes, veiculo_placa, frequencia, setor]):
                return JsonResponse({'error': 'Campos obrigatórios faltando'}, status=400)

            try:
                # Buscando os objetos no banco de dados
                motorista = Colaborador.objects.get(nome=motorista_nome, funcao="Motorista", status="ATIVO")
                print(f"Motorista encontrado: {motorista.nome}")  # Log
                coletores = Colaborador.objects.filter(nome__in=coletores_nomes, funcao="Coletor", status="ATIVO")
                print(f"Coletores encontrados: {[coletor.nome for coletor in coletores]}")  # Log
                veiculo = Veiculo.objects.get(placa_veiculo=veiculo_placa, status="Ativo")
                print(f"Veículo encontrado: {veiculo.placa_veiculo}")  # Log
            except ObjectDoesNotExist as e:
                print(f"Erro ao buscar objetos: {e}")  # Log do erro
                return JsonResponse({'error': 'Motorista, Coletor ou Veículo não encontrado ou inativo'}, status=404)

            # Função para converter hora para o formato adequado (YYYY-MM-DD HH:MM)
            def converter_para_data_hora(hora):
                try:
                    # Obter a data atual
                    data_atual = datetime.now().date()
                    # Adiciona a data atual e formata para o tipo de data-hora correto
                    return datetime.combine(data_atual, datetime.strptime(hora, '%H:%M').time())
                except ValueError:
                    return None  # Caso o formato da hora seja inválido

            # Convertendo as horas
            hora_entrega_chave = converter_para_data_hora(hora_entrega_chave)
            hora_entrega_saida_frota = converter_para_data_hora(hora_entrega_saida_frota)

            # Verificando se as conversões falharam
            if not hora_entrega_chave or not hora_entrega_saida_frota:
                return JsonResponse({'error': 'Formato de hora inválido'}, status=400)

            try:
                # Criando a soltura
                soltura = Soltura.objects.create(
                    motorista=motorista,
                    veiculo=veiculo,
                    frequencia=frequencia,
                    setores=setor,
                    celular=user.celular if user else "",  # Celular é enviado se o usuário for encontrado
                    lider=nome_lider,
                    hora_entrega_chave=hora_entrega_chave,
                    hora_entrega_saida_frota=hora_entrega_saida_frota
                )
                print(f"Soltura criada: {soltura.id}")  # Log da soltura criada

                # Limita a 3 coletores
                soltura.coletores.set(coletores[:3])
                print(f"Coletores associados: {[coletor.nome for coletor in soltura.coletores.all()]}")  # Log dos coletores

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
                }, status=201)
            except Exception as e:
                print(f"Erro ao criar soltura: {e}")  
                return JsonResponse({'error': 'Falha ao criar soltura'}, status=500)
                
        except json.JSONDecodeError:
            print("Erro de formato de dados JSON.") 
            return JsonResponse({'error': 'Formato de dados inválido'}, status=400)