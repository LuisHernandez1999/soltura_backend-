from django.http import JsonResponse
import logging
from ...service_soltura.service_count_rsu_pa_resume.resume_rsu_pa_service import contagem_geral_por_pa_rsu  
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)
@csrf_exempt
def contagem_geral_por_pa_view(request):
    try:
        resultado = contagem_geral_por_pa_rsu()
        return JsonResponse(resultado, status=200)
    except ValueError as ve:
        logger.warning(f"valor invalido ao processar contagem por PA: {str(ve)}")
        return JsonResponse({'erro': 'dados invalidos fornecidos.'}, status=400)
    except Exception as e:
        logger.error(f"erro inesperado na contagem geral por PA: {str(e)}", exc_info=True)
        return JsonResponse({'erro': 'erro interno no servidor.'}, status=500)

    
