from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django.http import JsonResponse
from datetime import date
from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def obter_solturas_seletiva_por_dia_da_semana(request):  # Adiciona o parâmetro `request`
    hoje = date.today()
    semana_atual = hoje.isocalendar().week
    ano_atual = hoje.year

    try:
        dados = (
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

        resultado = {dias_semana[i]: 0 for i in range(1, 8)}
        for entrada in dados:
            nome_dia = dias_semana.get(entrada['dia_semana'], 'Desconhecido')
            resultado[nome_dia] = entrada['total']

        logger.info("Contagem de solturas seletivas por dia da semana: %s", resultado)
        return JsonResponse(resultado)

    except Exception as e:
        logger.exception("Erro ao buscar solturas por dia da semana seletiva.")
        return JsonResponse(
            {"erro": f"Erro ao buscar solturas por dia da semana seletiva: {str(e)}"},
            status=500
        )
