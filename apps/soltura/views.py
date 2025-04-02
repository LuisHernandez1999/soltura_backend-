import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo
from django.core.cache import cache
import logging
from django.utils import timezone

import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo

logger = logging.getLogger(__name__)
@csrf_exempt
def cadastrar_soltura(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)

    try:
        data = json.loads(request.body)
        logger.info(f"Dados recebidos: {data}")

        required_fields = {
            'motorista', 'coletores', 'veiculo', 'frequencia', 'setor', 
            'hora_entrega_chave', 'hora_saida_frota', 'tipo_coleta', 'turno'
        }
        
        if not required_fields.issubset(data):
            return JsonResponse({'error': 'Campos obrigatórios faltando'}, status=400)

        # Buscar motorista e veículo com `select_related()` para evitar múltiplas queries
        motorista = Colaborador.objects.filter(
            nome=data['motorista'], funcao="Motorista", status="ATIVO"
        ).select_related().first()

        veiculo = Veiculo.objects.filter(
            placa_veiculo=data['veiculo'], status="Ativo"
        ).select_related().first()

        
        coletores = list(Colaborador.objects.filter(
            nome__in=data['coletores'], funcao="Coletor", status="ATIVO"
        )[:3])

        if not motorista or not veiculo or not coletores:
            return JsonResponse({'error': 'Motorista, Coletor ou Veículo não encontrado ou inativo'}, status=404)

       
        def converter_para_data_hora(valor):
            formatos = [
                '%H:%M', '%H:%M:%S', '%d/%m/%Y %H:%M', 
                '%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'
            ]
            for formato in formatos:
                try:
                    dt = datetime.strptime(valor, formato)
                    return timezone.make_aware(dt, timezone.get_default_timezone())  # Adiciona timezone
                except ValueError:
                    continue  

            raise ValueError(f"Formato de data/hora inválido: {valor}")

        hora_entrega_chave = converter_para_data_hora(data['hora_entrega_chave'])
        hora_saida_frota = converter_para_data_hora(data['hora_saida_frota'])

        # Criar a soltura
        soltura = Soltura.objects.create(
            motorista=motorista, 
            veiculo=veiculo, 
            frequencia=data['frequencia'], 
            setores=data['setor'],
            celular=data.get('celular', ''), 
            lider=data.get('lider', ''), 
            hora_entrega_chave=hora_entrega_chave,
            hora_saida_frota=hora_saida_frota, 
            tipo_coleta=data['tipo_coleta'], 
            turno=data['turno']
        )
        soltura.coletores.set(coletores)

        return JsonResponse({
            "motorista": motorista.nome,
            "matricula_motorista": motorista.matricula,
            "coletores": [coletor.nome for coletor in coletores],  # Correção aqui
            "placa_veiculo": veiculo.placa_veiculo,
            "frequencia": soltura.frequencia,
            "setores": soltura.setores,
            "celular": soltura.celular,
            "lider": soltura.lider,
            "hora_entrega_chave": hora_entrega_chave.strftime('%Y-%m-%d %H:%M:%S'),
            "hora_saida_frota": hora_saida_frota.strftime('%Y-%m-%d %H:%M:%S'),
            "tipo_coleta": soltura.tipo_coleta,
            "turno": soltura.turno
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Formato de dados inválido'}, status=400)
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao criar soltura: {e}")
        return JsonResponse({'error': 'Falha ao criar soltura'}, status=500)


logger = logging.getLogger(__name__)
@csrf_exempt
@csrf_exempt
def visualizar_solturas(request):
    if request.method == 'GET':  
        try:
            cache_key = "solturas_cache"
            solturas = cache.get_or_set(cache_key, lambda: list(
                Soltura.objects.select_related('motorista', 'veiculo')
                .values('id', 'motorista__nome', 'veiculo__placa', 'frequencia', 'setor',
                        'hora_entrega_chave', 'hora_saida_frota', 'tipo_coleta', 'turno')
            ), timeout=3600)

            return JsonResponse(solturas, safe=False)

        except Exception as e:
            logger.error(f"Erro ao buscar solturas: {e}")
            return JsonResponse({'error': 'Erro interno'}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)
           