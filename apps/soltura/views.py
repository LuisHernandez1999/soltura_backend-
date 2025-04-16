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
from django.views.decorators.http import require_GET
import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo
from datetime import date
import traceback

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
        if tipo_servico != 'varrição':
            required_fields.add('coletores')

        if not required_fields.issubset(data):
            return JsonResponse({'error': 'Campos obrigatórios faltando'}, status=400)

        motorista = Colaborador.objects.filter(
            nome=data['motorista'], funcao="Motorista",
             status__in=["ATIVO", "Ativo"]
        ).first()

        prefixo = data.get('veiculo') or data.get('prefixo')
        veiculo = Veiculo.objects.filter(
        prefixo=prefixo, 
        status__in=["ATIVO", "Ativo"]
        ).first()

        if not motorista or not veiculo:
            return JsonResponse({'error': 'motorista ou veiculo nao encontrado ou inativo'}, status=404)

        coletores = []
        if tipo_servico != 'varrição':
            coletores = list(Colaborador.objects.filter(
                nome__in=data['coletores'], funcao="Coletor", status="ATIVO"
            )[:3])

            if not coletores:
                return JsonResponse({'error': 'coletores nao encontrados ou inativos'}, status=404)

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
        hora_chegada_raw = data.get('hora_chegada')  # Tenta pegar o valor de hora_chegada
        hora_chegada = converter_para_data_hora(hora_chegada_raw) if hora_chegada_raw else None

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
            hora_chegada= hora_chegada,
            tipo_servico=data['tipo_servico'],
            rota=data.get('rota') or None
        )

        if coletores:
            soltura.coletores.set(coletores)

        return JsonResponse({
            "motorista": motorista.nome,
            "matricula_motorista": motorista.matricula,
            "coletores": [coletor.nome for coletor in coletores],
            "placa_veiculo": veiculo.prefixo,
            "frequencia": soltura.frequencia,
            "setores": soltura.setores,
            "celular": soltura.celular,
            "hora_chegada":hora_chegada,
            "lider": soltura.lider,
            "hora_entrega_chave": hora_entrega_chave.strftime('%Y-%m-%d %H:%M:%S'),
            "hora_saida_frota": hora_saida_frota.strftime('%Y-%m-%d %H:%M:%S'),
            "turno":soltura.turno,
            "rota":soltura.rota,
            "tipo_servico": soltura.tipo_servico,
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'formato de dados invalido'}, status=400)
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    except Exception as e:
       logger.error(f"Erro ao criar soltura: {e}")
       traceback.print_exc()  
    return JsonResponse({'error': 'Falha ao criar soltura'}, status=500)

logger = logging.getLogger(__name__)

@csrf_exempt
def exibir_solturas_registradas(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'metodo nao permitido'}, status=405)

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
                "prefixo": soltura.veiculo.prefixo,
                "frequencia": soltura.frequencia,
                "setores": soltura.setores,
                "celular": soltura.celular,
                "lider": soltura.lider,
                "hora_entrega_chave": soltura.hora_entrega_chave.strftime('%H:%M:%S') if soltura.hora_entrega_chave else None,
                "hora_saida_frota": soltura.hora_saida_frota.strftime('%H:%M:%S') if soltura.hora_saida_frota else None,
                "tipo_servico": soltura.tipo_servico,
                "turno": soltura.turno,
                "rota": soltura.rota,

            })
        return JsonResponse(resultados, safe=False, status=200)
    except Exception as e:
        logger.error(f"erro ao buscar solturas: {e}")
        return JsonResponse({'error': 'deu erro  no mapeamneto das  solturas'}, status=500)

@csrf_exempt
def exibir_total_de_remocao_soltas_no_dia(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'O método deve ser GET.'}, status=405)

    try:
        total_remocoes_hoje = Soltura.objects.filter(
            tipo_servico__iexact='Remoção'
        ).order_by('-data').values('motorista', 'veiculo').distinct().count()  

        print(f"Total de remoçoes mais recentes: {total_remocoes_hoje}")

        return JsonResponse({'total_remocoes': total_remocoes_hoje}, status=200)


    except Exception as e:
        logger.error(f"Erro ao buscar remoções: {e}")
        return JsonResponse({'error': f'erro ao buscar remoçoes: {str(e)}'}, status=500)


@csrf_exempt
def exibir_total_de_remocao_feitas(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'O método deve ser GET'}, status=405)

    try:
        total_remocoes = Soltura.objects.filter(
            tipo_servico__iexact='Remoção'
        ).values('motorista', 'veiculo', 'data').distinct().count()

        return JsonResponse({'total_remocoes_unicas': total_remocoes}, status=200)

    except Exception as e:
        return JsonResponse({'error': f'Erro ao buscar remoções: {str(e)}'}, status=500)



@csrf_exempt
def detalhes_de_todas_remocoes(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'metodo nao permitido'}, status=405)
    try:
        # Ajuste para evitar erro no distinct
        remocoes = Soltura.objects.select_related('motorista', 'veiculo') \
                                  .prefetch_related('coletores') \
                                  .filter(tipo_servico__iexact='Remoção') \
                                  .only(
                                      'motorista__nome', 'motorista__matricula',
                                      'veiculo__prefixo', 'frequencia', 'setores',
                                      'celular', 'lider', 'hora_entrega_chave',
                                      'hora_saida_frota', 'tipo_servico',
                                      'turno', 'rota'
                                  ).distinct()  # Apenas um distinct simples

        dados_todas_remocoes = []
        for soltura in remocoes:
            dados_todas_remocoes.append({
                "motorista": soltura.motorista.nome if soltura.motorista else None,
                "matricula_motorista": soltura.motorista.matricula if soltura.motorista else None,
                "coletores": [coletor.nome for coletor in soltura.coletores.all()],
                "prefixo": soltura.veiculo.prefixo if soltura.veiculo else None,
                "frequencia": soltura.frequencia,
                "setores": soltura.setores,
                "celular": soltura.celular,
                "lider": soltura.lider,
                "hora_entrega_chave": soltura.hora_entrega_chave.strftime('%H:%M:%S') if soltura.hora_entrega_chave else None,
                "hora_saida_frota": soltura.hora_saida_frota.strftime('%H:%M:%S') if soltura.hora_saida_frota else None,
                "tipo_servico": soltura.tipo_servico,
                "turno": soltura.turno,
                "rota": soltura.rota,
            })

        return JsonResponse({'remocoes': dados_todas_remocoes}, status=200, safe=False)

    except Exception as e:
        return JsonResponse({'error': 'Erro ao buscar todas remocoes'}, status=500)


@csrf_exempt
def detalhes_remocoes_hoje(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'metodo nao permitido'}, status=405)
    try:
        hoje = date.today()
        remocoes_hoje = Soltura.objects.select_related('motorista', 'veiculo') \
                                       .prefetch_related('coletores') \
                                       .filter(
                                           tipo_servico__iexact='Remoção',
                                           data=hoje
                                       ).only(
                                           'motorista__nome', 'motorista__matricula',
                                           'veiculo__prefixo', 'frequencia', 'setores',
                                           'celular', 'lider', 'hora_entrega_chave',
                                           'hora_saida_frota', 'tipo_servico',
                                           'turno', 'rota'
                                       ).distinct()  

        dados_remocoes_hoje = []
        for soltura in remocoes_hoje:
            dados_remocoes_hoje.append({
                "motorista": soltura.motorista.nome if soltura.motorista else None,
                "matricula_motorista": soltura.motorista.matricula if soltura.motorista else None,
                "coletores": [coletor.nome for coletor in soltura.coletores.all()],
                "prefixo": soltura.veiculo.prefixo if soltura.veiculo else None,
                "frequencia": soltura.frequencia,
                "setores": soltura.setores,
                "celular": soltura.celular,
                "lider": soltura.lider,
                "hora_entrega_chave": soltura.hora_entrega_chave.strftime('%H:%M:%S') if soltura.hora_entrega_chave else None,
                "hora_saida_frota": soltura.hora_saida_frota.strftime('%H:%M:%S') if soltura.hora_saida_frota else None,
                "tipo_servico": soltura.tipo_servico,
                "turno": soltura.turno,
                "rota": soltura.rota,
            })

        return JsonResponse({'remocoes_hoje': dados_remocoes_hoje}, status=200, safe=False)

    except Exception as e:
        return JsonResponse({'error': 'erro ao buscar remocoes de hoje'}, status=500)


        



            