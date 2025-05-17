from django.http import JsonResponse
from django.views.decorators.http import require_GET
from ...service_soltura.service_rsu_pa_exit.rsu_pa_exit_service import contar_solturas_rsu_por_garagem
import logging

logger = logging.getLogger(__name__)
@require_GET
def view_solturas_por_garagem(_):
    try:
        resultado = contar_solturas_rsu_por_garagem()
        return JsonResponse(resultado, status=200)

    except ValueError as ve:
        logger.warning(f"valor invalido ao processar a requisicao: {ve}")
        return JsonResponse({'error': 'parametro invalido fornecido.'}, status=400)

    except PermissionError as pe:
        logger.warning(f"Acesso negado: {pe}")
        return JsonResponse({'error': 'Acesso negado.'}, status=403)

    except TimeoutError as te:
        logger.error(f"tempo de resposta esgotado: {te}")
        return JsonResponse({'error': 'tempo de resposta esgotado'}, status=504)

    except Exception as e:
        logger.exception("erro inesperado ao buscar solturas por garagem")
        return JsonResponse({'error': 'erro interno no servidor. '}, status=500)
