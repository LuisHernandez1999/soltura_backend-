import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo
from django.utils import timezone
import json
from datetime import datetime
import traceback

@csrf_exempt
def cadastrar_soltura(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'metodo nao permitido'}, status=405)

    try:
        data = json.loads(request.body)
        logger.info(f"Dados recebidos: {data}")

        tipo_servico = data.get('tipo_servico', '').lower()

        required_fields = {
            'motorista', 'veiculo', 'frequencia', 
            'hora_entrega_chave', 'hora_saida_frota', 'turno', 'tipo_servico','tipo_equipe','status_frota'
        }
        if tipo_servico != 'varrição':
            required_fields.add('coletores')

        missing_fields = required_fields - data.keys()
        
        if missing_fields:
            logger.warning(f"campos obrigatorios faltando: {missing_fields}")
            return JsonResponse(
                {'error': 'campos obrigatorios faltando', 'missing_fields': list(missing_fields)},
                status=400
            )

        motorista = Colaborador.objects.filter(
            nome=data['motorista'],
            funcao="Motorista",
            status__in=["ATIVO", "Ativo"]
        ).first()

        prefixo = data.get('veiculo') or data.get('prefixo')
        veiculo = Veiculo.objects.filter(
            prefixo=prefixo,
            status__in=["ATIVO", "Ativo"]
        ).first()

        if not motorista or not veiculo:
            logger.warning("motorista ou veículo nao encontrado ou inativo.")
            return JsonResponse({'error': 'motorista ou veiculo nao encontrado ou inativo'}, status=404)

        coletores = []
        if tipo_servico != 'varrição':
            coletores = list(Colaborador.objects.filter(
                nome__in=data['coletores'],
                funcao="Coletor",
                status="ATIVO"
            )[:3])

            if not coletores:
                logger.warning("coletores nao encontrados ou inativos.")
                return JsonResponse({'error': 'coletores nao encontrados ou inativos'}, status=404)

        def converter_para_data_hora(valor):
            formatos = [
                '%H:%M', '%H:%M:%S', '%d/%m/%Y %H:%M',
                '%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%dT%H:%M:%SZ',
            ]
            for formato in formatos:
                try:
                    dt = datetime.strptime(valor, formato)
                    if dt.year < 2024:
                        raise ValueError(f"data anterior a 2025 nao vai ze: {valor}")
                    if formato in ['%H:%M', '%H:%M:%S']:
                        raise ValueError(f"formato de hora errado sem data completa: {valor}")
                    return timezone.make_aware(dt, timezone.get_default_timezone())
                except ValueError:
                    continue
            raise ValueError(f"formato de data/hora erradas ou data anterior a 2025: {valor}")
        

        status_frota = data.get('status_frota')
        if status_frota == 'Em Andamento':
                hora_chegada = None        

        hora_entrega_chave = converter_para_data_hora(data['hora_entrega_chave'])
        hora_saida_frota = converter_para_data_hora(data['hora_saida_frota'])
        hora_chegada_raw = data.get('hora_chegada')
        hora_chegada = converter_para_data_hora(hora_chegada_raw) if hora_chegada_raw else None 

       #### evita cadastros repetidos 
        data_saida = hora_saida_frota.date()
        soltura_duplicada = Soltura.objects.filter(
            motorista=motorista,
            data=data_saida,
            hora_saida_frota=hora_saida_frota
        ).exists()

        if soltura_duplicada:
            logger.warning(f"duplicacao de soltura detectada para motorista {motorista.nome} em {hora_saida_frota}")
            return JsonResponse({
                'error': 'ja existe um cadastro com esse motorista e essa hora de saida hoje.'
            }, status=400)

        soltura = Soltura.objects.create(
            motorista=motorista,
            veiculo=veiculo,
            data= data['data'],
            tipo_equipe = data['tipo_equipe'],
            frequencia=data['frequencia'],
            garagem= data['garagem'],
            celular=data.get('celular', ''),
            lider=data.get('lider', ''),
            hora_entrega_chave=hora_entrega_chave,
            hora_saida_frota=hora_saida_frota,
            turno=data['turno'],
            hora_chegada=hora_chegada,
            tipo_servico=data['tipo_servico'],
            rota=data.get('rota') or None,
            status_frota = data.get('status_frota')
        )

        if coletores:
            soltura.coletores.set(coletores)

        logger.info(f"soltura criada com sucesso para motorista {motorista.nome}")

        return JsonResponse({
            "motorista": motorista.nome,
            "tipo_equipe": soltura.tipo_equipe,            
            "matricula_motorista": motorista.matricula,
            "coletores": [coletor.nome for coletor in coletores],
            "data":soltura.data,
            "placa_veiculo": veiculo.prefixo,
            "frequencia": soltura.frequencia,
            "setores": soltura.setores,
            "celular": soltura.celular,
            "hora_chegada": hora_chegada,
            "lider": soltura.lider,
            "hora_entrega_chave": hora_entrega_chave.strftime('%Y-%m-%d %H:%M:%S'),
            "hora_saida_frota": hora_saida_frota.strftime('%Y-%m-%d %H:%M:%S'),
            "turno": soltura.turno,
            "rota": soltura.rota,
            "tipo_servico": soltura.tipo_servico,
            "status_frota": soltura.status_frota
        }, status=201)

    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logger.exception("Erro inesperado ao cadastrar soltura")
        return JsonResponse({'error': 'Erro interno no servidor'}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'formato de dados invalido'}, status=400)
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    except Exception as e:
       logger.error(f"Erro ao criar soltura: {e}")
       traceback.print_exc()  
    return JsonResponse({'error': 'falha ao criar soltura'}, status=500)
    
logger = logging.getLogger(__name__)