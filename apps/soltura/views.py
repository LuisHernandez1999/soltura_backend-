import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo
import logging
from django.utils import timezone
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo
from datetime import date
import traceback
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.utils.timezone import now
import calendar
from django.utils.timezone import make_aware
from django.utils.timezone import localdate

logger = logging.getLogger(__name__)

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
                    if dt.year < 2025:
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
                "tipo_equipe": soltura.tipo_equipe, 
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
                "status_frota": soltura.status_frota

            })
        return JsonResponse(resultados, safe=False, status=200)
    except Exception as e:
        logger.error(f"erro ao buscar solturas: {e}")
        return JsonResponse({'error': 'deu erro  no mapeamneto das  solturas'}, status=500)

@csrf_exempt
def editar_soltura(request, soltura_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'metodo nao permitido'}, status=405)

    try:
        # Carregar dados da requisição
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


@csrf_exempt
def exibir_total_de_remocao_soltas_no_dia(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'o metodo deve ser GET.'}, status=405)

    try:
        hoje = now().date()

        total_remocoes_hoje = Soltura.objects.filter(
            tipo_servico__iexact='Remoção',
            data=hoje
        ).values('motorista', 'veiculo').distinct().count()

        logger.info(f"total de remocoes feitas hoje ({hoje}): {total_remocoes_hoje}")
        return JsonResponse({'total_remocoes': total_remocoes_hoje}, status=200)

    except Exception as e:
        logger.error(f"erro ao buscar remocoes: {e}")
        return JsonResponse({'error': f'Erro ao buscar remocoes: {str(e)}'}, status=500)



@csrf_exempt
def exibir_total_de_remocao_feitas(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'metodo nao permitido. Use GET.'}, status=405)

    try:
        total_remocoes = Soltura.objects.filter(
            tipo_servico__iexact='Remoção',
            data__isnull=False
        ).count()

        return JsonResponse({'total_remocoes': total_remocoes}, status=200)

    except Exception as e:
        return JsonResponse({'error': 'erro ao buscar remocoes.', 'detalhes': str(e)}, status=500)



@csrf_exempt
def detalhes_de_todas_remocoes(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'metodo nao permitido'}, status=405)
    try:

        remocoes = Soltura.objects.select_related('motorista', 'veiculo') \
                                  .prefetch_related('coletores') \
                                  .filter(tipo_servico__iexact='Remoção') \
                                  .only(
                                      'motorista__nome', 'motorista__matricula',
                                      'veiculo__prefixo', 'frequencia', 'setores',
                                      'celular', 'lider', 'hora_entrega_chave',
                                      'hora_saida_frota', 'tipo_servico',
                                      'turno', 'rota'
                                  ).distinct()  # apenas um distinct simples

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
        return JsonResponse({'error': 'erro ao buscar todas remocoes'}, status=500)


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


@csrf_exempt
def media_mensal_de_solturas(request):  ##### media de solturas por mes 
    if request.method != 'GET':
        return JsonResponse({'error': 'aqui deve ser GET'}, status=405)
    try:
        ano_atual = datetime.now().year
        dados = (
            Soltura.objects
            .filter(data__year=ano_atual)
            .annotate(mes=ExtractMonth('data'))
            .values('mes')
            .annotate(total=Count('id'))
        )
        totais_por_mes = {mes: 0 for mes in range(1, 13)}
        for entrada in dados:
            totais_por_mes[entrada['mes']] = entrada['total']

        media = sum(totais_por_mes.values()) / 12

        return JsonResponse({'media_mensal_de_solturas': round(media, 2)}, status=200)

    except Exception as e:
        return JsonResponse({'error': f'erro ao calcular media de solturas: {str(e)}'}, status=500)

@csrf_exempt 
def remocoe_por_mes(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'aqui deve ser GET'}, status=405)
    try:
        ano_atual = datetime.now().year
        resultado = {}

        for mes in range(1, 13):
            inicio_mes = make_aware(datetime(ano_atual, mes, 1))
            if mes == 12:
                fim_mes = make_aware(datetime(ano_atual + 1, 1, 1))
            else:
                fim_mes = make_aware(datetime(ano_atual, mes + 1, 1))

            total = Soltura.objects.filter(
                tipo_servico__iexact='Remoção',
                data__gte=inicio_mes,
                data__lt=fim_mes
            ).count()

            nome_mes = calendar.month_name[mes]
            resultado[nome_mes] = total

        return JsonResponse({'remocoes_por_mes': resultado}, status=200)

    except Exception as e:
        logger.error(f"erro ao buscar remocoes por mes: {e}")
        return JsonResponse({'error': f'erro ao buscar dados: {str(e)}'}, status=500)

@csrf_exempt
def quantidade_soltura_equipes_dia(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'metodo nao permitido deve ser GET zeca'}, status=405)
    try:
        hoje = localdate()  

        resultado = (
            Soltura.objects
            .filter(data=hoje, tipo_servico='Remoção') 
            .values('tipo_equipe')
            .annotate(quantidade=Count('id'))
            .order_by('tipo_equipe')
        )

        return JsonResponse({'dados': list(resultado)}, status=200)
    except Exception as e:
        return JsonResponse({'error': f' deu erro ao contar solturas por equipe, olha a filtragem e vallores como ta na model : {str(e)}'}, status=500)
       