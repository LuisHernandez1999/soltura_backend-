from django.http import JsonResponse
from django.views.decorators.http import require_GET
from ...service_soltura.service_coletores_motorista_rsu.turno_rsu_service import quantidade_motorista_coletores_equipe
import logging

logger = logging.getLogger(__name__)

@require_GET
def view_qtd_motoristas_coletores_por_equipe(request):
    try:
        logger.info("requisicao recebida para obter quantidade de motoristas e coletores por equipe RSU.")

        resultado = quantidade_motorista_coletores_equipe()

        if not resultado:
            logger.warning("nenhum dado encontrado para as equipes RSU no dia atual.")
            return JsonResponse({'message': 'nenhum dado encontrado para as equipes RSU hoje.'}, status=204)

        logger.info("dados retornados com sucesso: %s", resultado)
        return JsonResponse(resultado, status=200)

    except ValueError as ve:
        logger.error("erro de valor na requisicao: %s", str(ve))
        return JsonResponse({'error': f'Erro de valor: {str(ve)}'}, status=400)

    except KeyError as ke:
        logger.error("erro de chave na requisicao: %s", str(ke))
        return JsonResponse({'error': f'chave invalida: {str(ke)}'}, status=400)

    except Exception as e:
        logger.exception("erro inesperado ao processar a requisicao.")
        return JsonResponse({'error': f'erro interno no servidor: {str(e)}'}, status=500)
