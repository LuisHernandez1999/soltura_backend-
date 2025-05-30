from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django.http import JsonResponse
from datetime import date
from apps.soltura.models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def dashboard_seletiva_dados_tabela_grafico(request):
    hoje = date.today()
    semana_atual = hoje.isocalendar().week
    ano_atual = hoje.year

    # Configuração para 100 páginas com 100 registros por página
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 100))  # Padrão 100 por página
    
    # Limitar a 100 solturas por página (máximo)
    if page_size > 100:
        page_size = 100
    if page_size < 1:
        page_size = 1
    
    # Limitar a 100 páginas máximo
    max_pages = 100

    try:
        # Consulta agregada: quantidade por dia da semana (semana atual para o gráfico)
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

        # Consulta detalhada - TODOS OS REGISTROS
        queryset = (
            Soltura.objects
            .filter(tipo_servico__iexact='Seletiva')
            .select_related('motorista', 'veiculo')
            .prefetch_related('coletores')
            .order_by('-data', '-hora_saida_frota')
        )

        # Limitar o total de registros para não exceder 100 páginas
        total_registros = queryset.count()
        max_registros = max_pages * page_size  # 100 páginas × 100 registros = 10.000 registros máximo
        
        if total_registros > max_registros:
            # Limitar o queryset aos primeiros 10.000 registros (mais recentes)
            queryset = queryset[:max_registros]
            logger.info(f"Limitando resultados a {max_registros} registros mais recentes (100 páginas × 100 por página)")

        paginator = Paginator(queryset, page_size)

        # Verificar se a página solicitada não excede 100
        if page > max_pages:
            page = max_pages
        
        try:
            solturas_pagina = paginator.page(page)
        except PageNotAnInteger:
            solturas_pagina = paginator.page(1)
        except EmptyPage:
            # Se não há dados suficientes, ir para a última página disponível
            ultima_pagina = min(paginator.num_pages, max_pages)
            solturas_pagina = paginator.page(ultima_pagina)

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

        # Calcular páginas limitadas a 100
        total_paginas_real = paginator.num_pages
        total_paginas_limitado = min(total_paginas_real, max_pages)

        resultado = {
            'resumo_por_dia_da_semana': resumo_por_dia,
            'detalhes_solturas': lista_detalhada,
            'configuracao': {
                'max_pages': max_pages,
                'max_registros_por_pagina': 100,
                'total_registros_disponiveis': total_registros,
                'registros_sendo_exibidos': min(total_registros, max_registros)
            },
            'paginacao': {
                'pagina_atual': solturas_pagina.number,
                'total_paginas': total_paginas_limitado,
                'total_paginas_real': total_paginas_real,
                'total_solturas': min(paginator.count, max_registros),
                'total_solturas_real': total_registros,
                'page_size': int(page_size),
                'tem_proxima': solturas_pagina.has_next() and solturas_pagina.number < max_pages,
                'tem_anterior': solturas_pagina.has_previous(),
                'primeira_pagina': 1,
                'ultima_pagina': total_paginas_limitado,
                'registros_na_pagina': len(lista_detalhada),
                'limitado_a_100_paginas': total_paginas_real > max_pages
            }
        }

        logger.info(f"Dados seletiva - página {page} de {total_paginas_limitado} (limitado a 100 páginas). Registros na página: {len(lista_detalhada)}")
        return JsonResponse(resultado, safe=False)

    except Exception as e:
        logger.exception("Erro ao obter dados seletiva paginados.")
        return JsonResponse({'erro': f'Erro: {str(e)}'}, status=500)