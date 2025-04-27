# views/soltura_views.py
from django.http import JsonResponse
from ...service_soltura.service_team_pie.pie_team_service import quantidade_solturas_por_equipe_dia
import logging

logger = logging.getLogger(__name__)

def quantidade_solturas_por_equipe_view(request):
    try:
        resultado = quantidade_solturas_por_equipe_dia()
        return JsonResponse(resultado, safe=False, status=200)
    except Exception as e:
        logger.error(f"Erro na view de quantidade de solturas por equipe: {e}")
        return JsonResponse({'error': 'Erro ao buscar quantidade de solturas por equipe'}, status=500)
