from django.http import JsonResponse
import logging

from ...service_soltura.service_seletiva_dashboard.get_soltura_grafic_table import dashboard_seletiva_dados_tabela_grafico

logger = logging.getLogger(__name__)

def dashboard_seletiva_dados_tabela_grafic(request):
    try:
        return dashboard_seletiva_dados_tabela_grafico(request)
    except Exception as e:
        logger.exception("Erro ao obter dados seletiva paginados.")
        return JsonResponse({'erro': f'Erro: {str(e)}'}, status=500)