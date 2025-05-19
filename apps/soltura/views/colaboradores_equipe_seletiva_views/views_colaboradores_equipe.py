from django.http import JsonResponse
from django.views.decorators.http import require_GET
import logging

from ...service_soltura.service_seletiva_coletores_motoristas.seletiva_coletores_motoristas_service import contar_coletores_motorista_por_turno

logger = logging.getLogger(__name__)

@require_GET
def view_contar_coletores_motorista_por_turno(request):
    try:
        resultado = contar_coletores_motorista_por_turno()
        return JsonResponse({
            'status': 'sucesso',
            'dados': resultado
        }, status=200)

    except ValueError as ve:
        logger.warning("erro de valor ao contar dados: %s", ve)
        return JsonResponse({
            'status': 'erro',
            'mensagem': 'erro de valor nos dados recebidos.',
            'detalhes': str(ve)
        }, status=400)

    except Exception as e:
        logger.error("erro inesperado ao contar coletores/motoristas: %s", e)
        return JsonResponse({
            'status': 'erro',
            'mensagem': 'erro interno ao processar os dados.',
            'detalhes': str(e)
        }, status=500)
