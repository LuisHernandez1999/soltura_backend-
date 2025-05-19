import logging
import traceback
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import DatabaseError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ...service_soltura.service_seletiva_cards.cards_seletiva_service import contar_seletiva_realizadas_hoje

logger = logging.getLogger(__name__)

@api_view(['GET'])
def seletivas_realizadas_hoje(request):
    try:
        total = contar_seletiva_realizadas_hoje()
        return Response({'total_seletivas_hoje': total}, status=status.HTTP_200_OK)

    except ObjectDoesNotExist as e:
        logger.warning(f"ojeto nao encontrado: {e}")
        return Response(
            {'erro': 'algum recurso necessario nao foi encontrado.', 'detalhes': str(e)},
            status=status.HTTP_404_NOT_FOUND
        )

    except ValidationError as e:
        logger.warning(f"erro de validacao: {e}")
        return Response(
            {'erro': 'dados invalidos.', 'detalhes': e.message_dict if hasattr(e, 'message_dict') else str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

    except (ValueError, TypeError) as e:
        logger.warning(f"erro de valor ou tipo: {e}")
        return Response(
            {'erro': 'erro de tipo ou valor.', 'mensagem': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

    except DatabaseError as e:
        logger.error(f"erro de banco de dados: {e}")
        logger.debug(traceback.format_exc())
        return Response(
            {'erro': 'erro ao acessar o banco de dados.', 'mensagem': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:
        logger.critical("erro inesperado ao buscar seletivas.")
        logger.debug(traceback.format_exc())
        return Response(
            {
                'erro': 'erro interno inesperado.',
                'mensagem': str(e),
                'tipo': type(e).__name__,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
