from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_GET
from ...service_soltura.service_rsu_grafic.grafic_rsu_service import solturas_por_dia_da_semana_rsu
import logging

logger = logging.getLogger(__name__)

@require_GET
def view_solturas_por_dia_da_semana_rsu(request):
    if request.method != 'GET':
        logger.warning(f"metodo HTTP invalido: {request.method}")
        return HttpResponseNotAllowed(['GET'], "metodo HTTP nao permitido. Use GET.")
    
    try:
        resultado = solturas_por_dia_da_semana_rsu()
        if not resultado:
            logger.warning("service retornou resultado vazio ou None.")
            return JsonResponse({'message': 'nenhum dado encontrado para solturas RSU.'}, status=204)
        if not isinstance(resultado, dict):
            logger.error(f"resultado inesperado do service: {type(resultado)}")
            return JsonResponse({'error': 'Formato de dado inesperado.'}, status=500)
        
        return JsonResponse({'solturas_por_dia_da_semana_rsu': resultado}, status=200)
    
    except ValueError as ve:
        logger.error(f"erro de valor na view: {ve}", exc_info=True)
        return JsonResponse({'error': f'erro de valor: {str(ve)}'}, status=400)
    except KeyError as ke:
        logger.error(f"chave esperada nao encontrada: {ke}", exc_info=True)
        return JsonResponse({'error': f'erro interno: chave invalida {str(ke)}'}, status=500)
    except Exception as e:
        logger.error(f"erro inesperado na view: {e}", exc_info=True)
        return JsonResponse({'error': 'erro interno ao processar a solicitacao'}, status=500)
