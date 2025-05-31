from django.http import JsonResponse
import logging

from ...service_soltura.service_rsu_dashboard.rsu_table_grafic_service import dashboard_rsu_dados_tabela_grafico

logger = logging.getLogger(__name__)

def dashboard_rsu_dados_tabela_grafic_view(request):
    try:
        return dashboard_rsu_dados_tabela_grafico(request)
    except Exception as e:
        logger.exception("Erro ao obter dados seletiva paginados.")
        return JsonResponse({'erro': f'Erro: {str(e)}'}, status=500)