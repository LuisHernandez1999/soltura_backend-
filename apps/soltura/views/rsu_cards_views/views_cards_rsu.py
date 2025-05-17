from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.db import DatabaseError
from django.core.exceptions import ValidationError
from ...service_soltura.service_cards_rsu.cards_rsu_service import contar_rsu_realizadas_hoje
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_GET
def exibir_total_de_rsu_soltas_no_dia(request):
    logger.info(f"Usuário {request.user} iniciou contagem de RSUs.")

    try:
        total = contar_rsu_realizadas_hoje()

        logger.info(f"contagem concluida com sucesso: {total} RSUs.")
        return JsonResponse(
            {
                'status': 'sucesso',
                'mensagem': 'contagem de RSUs realizada com sucesso.',
                'dados': {'total_rsu': total}
            },
            status=200
        )

    except ValidationError as e:
        logger.warning(f"erro de validacao nos parametros: {e}")
        return JsonResponse(
            {
                'status': 'erro',
                'mensagem': 'erro de validacao nos dados fornecidos.',
                'detalhes': e.message_dict if hasattr(e, 'message_dict') else str(e)
            },
            status=400
        )

    except DatabaseError as e:
        logger.error(f"Erro no banco de dados: {e}")
        return JsonResponse(
            {
                'status': 'erro',
                'mensagem': 'erro interno ao acessar o banco de dados.',
                'detalhes': str(e)
            },
            status=500
        )

    except Exception as e:
        logger.exception("erro inesperado ao buscar contagem de RSUs.")
        return JsonResponse(
            {
                'status': 'erro',
                'mensagem': 'erro inesperado ao processar a requisicao.',
                'detalhes': str(e)
            },
            status=500
        )
