# apps/soltura/views/soltura_views.py

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.db import DatabaseError
import logging

from ...service_soltura.service_seletiva_tabela.tabela_seletiva_service import retornar_infos_seletiva

logger = logging.getLogger(__name__)

@require_GET
def solturas_seletiva_infos_view(request):
    try:
        dados = retornar_infos_seletiva()

        if not dados:
            logger.warning("nenhuma informacao de soltura seletiva encontrada.")
            return JsonResponse(
                {"message": "nenhuma soltura seletiva encontrada."},
                status=404
            )

        return JsonResponse({"solturas_seletiva": list(dados)}, status=200, safe=False)

    except FieldError as field_err:
        logger.error("erro de campo invalido na consulta: %s", str(field_err))
        return JsonResponse(
            {"error": f"campo invalido na consulta: {str(field_err)}"},
            status=400
        )

    except ObjectDoesNotExist:
        logger.warning("nenhum objeto Soltura correspondente encontrado.")
        return JsonResponse(
            {"error": "objeto Soltura nao encontrado."},
            status=404
        )

    except DatabaseError as db_err:
        logger.error("erro de banco de dados ao buscar solturas seletivas: %s", str(db_err))
        return JsonResponse(
            {"error": "erro ao acessar o banco de dados."},
            status=500
        )

    except Exception as e:
        logger.exception("erro inesperado ao processar a view de solturas seletivas.")
        return JsonResponse(
            {"error": "erro interno inesperado."},
            status=500
        )
