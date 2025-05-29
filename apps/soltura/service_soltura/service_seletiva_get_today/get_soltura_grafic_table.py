from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django.http import JsonResponse
from datetime import date
from models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def obter_dados_seletiva_completos_paginado(request):
    hoje = date.today()
    semana_atual = hoje.isocalendar().week
    ano_atual = hoje.year

    # Pegar parâmetros de paginação da query string (exemplo: ?page=2&page_size=20)
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 20)

    try:
        # Consulta agregada: quantidade por dia da semana na semana atual
        dados_aggregados = (
            Soltura.objects
            .filter(
                tipo_servico__iexact='Seletiva',
                data__week=semana_atual,
                data__year=ano_atual
            )
            .annotate(dia_semana=ExtractWeekDay('data'))
            .values('dia_semana')
            .annotate(total=Count('id'))
        )

        dias_semana = {
            1: 'Domingo',
            2: 'Segunda-feira',
            3: 'Terça-feira',
            4: 'Quarta-feira',
            5: 'Quinta-feira',
            6: 'Sexta-feira',
            7: 'Sábado',
        }

        resumo_por_dia = {dias_semana[i]: 0 for i in range(1, 8)}
        for entrada in dados_aggregados:
            nome_dia = dias_semana.get(entrada['dia_semana'], 'Desconhecido')
            resumo_por_dia[nome_dia] = entrada['total']

        # Consulta detalhada paginada
        queryset = (
            Soltura.objects
            .filter(tipo_servico__iexact='Seletiva')
            .select_related('motorista', 'veiculo')
            .prefetch_related('coletores')
            .order_by('-data', '-hora_saida_frota')  # Ordenação recente primeiro
        )

        paginator = Paginator(queryset, page_size)

        try:
            solturas_pagina = paginator.page(page)
        except PageNotAnInteger:
            solturas_pagina = paginator.page(1)
        except EmptyPage:
            solturas_pagina = paginator.page(paginator.num_pages)

        lista_detalhada = []
        for s in solturas_pagina:
            lista_detalhada.append({
                'id': s.id,
                'motorista': s.motorista.nome if s.motorista else None,
                'hora_saida_frota': s.hora_saida_frota.isoformat() if s.hora_saida_frota else None,
                'prefixo': s.veiculo.prefixo if s.veiculo else None,
                'hora_entrega_chave': s.hora_entrega_chave.isoformat() if s.hora_entrega_chave else None,
                'hora_chegada': s.hora_chegada.isoformat() if s.hora_chegada else None,
                'coletores': [c.nome for c in s.coletores.all()],
                'data': s.data.isoformat() if s.data else None,
                'lider': s.lider,
                'rota': s.rota,
                'tipo_equipe': s.tipo_equipe,
                'status_frota': s.status_frota,
                'tipo_veiculo_selecionado': s.tipo_veiculo_selecionado,
            })

        resultado = {
            'resumo_por_dia_da_semana': resumo_por_dia,
            'detalhes_solturas': lista_detalhada,
            'paginacao': {
                'pagina_atual': solturas_pagina.number,
                'total_paginas': paginator.num_pages,
                'total_solturas': paginator.count,
                'page_size': page_size,
                'tem_proxima': solturas_pagina.has_next(),
                'tem_anterior': solturas_pagina.has_previous(),
            }
        }

        logger.info(f"Dados seletiva paginados - página {page} obtidos com sucesso.")
        return JsonResponse(resultado, safe=False)

    except Exception as e:
        logger.exception("Erro ao obter dados seletiva paginados.")
        return JsonResponse({'erro': f'Erro: {str(e)}'}, status=500)
