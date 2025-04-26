import logging
from django.http import JsonResponse
from ...models.models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from apps.colaborador.models import Colaborador



@csrf_exempt
def editar_soltura(request, soltura_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'metodo nao permitido'}, status=405)

    try:
        data = json.loads(request.body)
        logger.info(f"dados recebidos para edicao: {data}")

        tipo_servico = data.get('tipo_servico', '').lower()

        required_fields = {
            'motorista', 'veiculo', 'frequencia', 'setor',
            'hora_entrega_chave', 'hora_saida_frota', 'turno', 'tipo_servico'
        }

        if tipo_servico != 'varrição':
            required_fields.add('coletores')

        missing_fields = required_fields - data.keys()

        if missing_fields:
            logger.warning(f"Campos obrigatórios faltando: {missing_fields}")
            return JsonResponse(
                {'error': 'Campos obrigatórios faltando', 'missing_fields': list(missing_fields)},
                status=400
            )

        soltura = Soltura.objects.filter(id=soltura_id).first()

        if not soltura:
            logger.warning(f"soltura nao encontrada com ID {soltura_id}")
            return JsonResponse({'error': 'soltura nao encontrada'}, status=404)

     
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
                    if dt.year < 2025:
                        raise ValueError(f"Data anterior a 2025 não é válida: {valor}")
                    if formato in ['%H:%M', '%H:%M:%S']:
                        raise ValueError(f"Formato de hora sem data completa: {valor}")
                    return timezone.make_aware(dt, timezone.get_default_timezone())
                except ValueError:
                    continue
            raise ValueError(f"Formato de data/hora inválido ou data anterior a 2025: {valor}")

       
        hora_entrega_chave = converter_para_data_hora(data['hora_entrega_chave'])
        hora_saida_frota = converter_para_data_hora(data['hora_saida_frota'])
        hora_chegada_raw = data.get('hora_chegada')
        hora_chegada = converter_para_data_hora(hora_chegada_raw) if hora_chegada_raw else None

       
        soltura.motorista = motorista
        soltura.veiculo = veiculo
        soltura.tipo_equipe = data['tipo_equipe']
        soltura.frequencia = data['frequencia']
        soltura.setores = data['setor']
        soltura.celular = data.get('celular', '')
        soltura.lider = data.get('lider', '')
        soltura.hora_entrega_chave = hora_entrega_chave
        soltura.hora_saida_frota = hora_saida_frota
        soltura.turno = data['turno']
        soltura.hora_chegada = hora_chegada
        soltura.tipo_servico = data['tipo_servico']
        soltura.rota = data.get('rota') or None
        soltura.data = data.get('data')
        soltura.status_frota = data.get('status_frota')

       
        if coletores:
            soltura.coletores.set(coletores)

       
        soltura.save()

        logger.info(f"soltura {soltura_id} editada com sucesso.")

        return JsonResponse({
            "motorista": motorista.nome,
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
        }, status=200)

    except ValueError as e:
        logger.error(f"erro de validacao: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logger.exception("erro inesperado ao editar soltura")
        return JsonResponse({'error': 'erro interno no servidor'}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'formato de dados invalido'}, status=400)
logger = logging.getLogger(__name__)