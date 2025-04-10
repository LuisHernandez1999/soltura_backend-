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

        tipo_servico = data.get('tipo_servico', '').lower()

        required_fields = {
            'motorista', 'veiculo', 'frequencia', 'setor',
            'hora_entrega_chave', 'hora_saida_frota', 'turno', 'tipo_servico'
        }

        # Apenas exigir coletores se não for varrição
        if tipo_servico != 'varrição':
            required_fields.add('coletores')

        if not required_fields.issubset(data):
            return JsonResponse({'error': 'Campos obrigatórios faltando'}, status=400)

        motorista = Colaborador.objects.filter(
            nome=data['motorista'], funcao="Motorista", status="ATIVO"
        ).first()

        veiculo = Veiculo.objects.filter(
            placa_veiculo=data['veiculo'], status="Ativo"
        ).first()

        if not motorista or not veiculo:
            return JsonResponse({'error': 'Motorista ou Veículo não encontrado ou inativo'}, status=404)

        coletores = []
        if tipo_servico != 'varrição':
            coletores = list(Colaborador.objects.filter(
                nome__in=data['coletores'], funcao="Coletor", status="ATIVO"
            )[:3])

            if not coletores:
                return JsonResponse({'error': 'Coletores não encontrados ou inativos'}, status=404)

        def converter_para_data_hora(valor):
            formatos = [
                '%H:%M', '%H:%M:%S', '%d/%m/%Y %H:%M',
                '%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'
            ]
            for formato in formatos:
                try:
                    dt = datetime.strptime(valor, formato)
                    return timezone.make_aware(dt, timezone.get_default_timezone())
                except ValueError:
                    continue
            raise ValueError(f"Formato de data/hora inválido: {valor}")

        hora_entrega_chave = converter_para_data_hora(data['hora_entrega_chave'])
        hora_saida_frota = converter_para_data_hora(data['hora_saida_frota'])

        soltura = Soltura.objects.create(
            motorista=motorista,
            veiculo=veiculo,
            frequencia=data['frequencia'],
            setores=data['setor'],
            celular=data.get('celular', ''),
            lider=data.get('lider', ''),
            hora_entrega_chave=hora_entrega_chave,
            hora_saida_frota=hora_saida_frota,
            turno=data['turno'],
            tipo_servico=data['tipo_servico'],
        )

        if coletores:
            soltura.coletores.set(coletores)

        return JsonResponse({
            "motorista": motorista.nome,
            "matricula_motorista": motorista.matricula,
            "coletores": [coletor.nome for coletor in coletores],
            "placa_veiculo": veiculo.placa_veiculo,
            "frequencia": soltura.frequencia,
            "setores": soltura.setores,
            "celular": soltura.celular,
            "lider": soltura.lider,
            "hora_entrega_chave": hora_entrega_chave.strftime('%Y-%m-%d %H:%M:%S'),
            "hora_saida_frota": hora_saida_frota.strftime('%Y-%m-%d %H:%M:%S'),
            "turno": soltura.turno,
            "tipo_servico": soltura.tipo_servico,
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
def exibir_solturas_registradas(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Método não permitido'}, status=405)

    try:
        placa = request.GET.get('placa_veiculo')  

        solturas = (
            Soltura.objects
            .select_related('motorista', 'veiculo')
            .prefetch_related('coletores')
            .order_by('-hora_saida_frota')  
        )

        if placa:
            solturas = solturas.filter(veiculo__placa_veiculo=placa)

        resultados = []

        for soltura in solturas:
            resultados.append({
                "motorista": soltura.motorista.nome,
                "matricula_motorista": soltura.motorista.matricula,
                "coletores": [coletor.nome for coletor in soltura.coletores.all()],
                "placa_veiculo": soltura.veiculo.placa_veiculo,
                "frequencia": soltura.frequencia,
                "setores": soltura.setores,
                "celular": soltura.celular,
                "lider": soltura.lider,
                "hora_entrega_chave": soltura.hora_entrega_chave.strftime('%Y-%m-%d %H:%M:%S') if soltura.hora_entrega_chave else None,
                "hora_saida_frota": soltura.hora_saida_frota.strftime('%Y-%m-%d %H:%M:%S') if soltura.hora_saida_frota else None,
                "tipo_servico": soltura.tipo_servico,
                "turno": soltura.turno
            })

        return JsonResponse(resultados, safe=False, status=200)

    except Exception as e:
        logger.error(f"Erro ao buscar solturas: {e}")
        return JsonResponse({'error': 'Erro ao buscar solturas'}, status=500)
           