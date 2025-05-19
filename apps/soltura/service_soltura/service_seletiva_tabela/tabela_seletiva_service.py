from django.http import JsonResponse
from apps.soltura.models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def retornar_infos_seletiva(request):
    try:
        seletiva_saidas_info = (
            Soltura.objects
            .filter(tipo_servico__iexact='Seletiva')
            .values(
                'motorista',
                'hora_saida_frota',  # corrigido aqui
                'hora_entrega_chave',
                'hora_chegada',
                'coletores',
                'data',
                'lider',
                'rota',
                'tipo_equipe',
                'status_frota',
                'tipo_veiculo_selecionado'
            )
        )
        return JsonResponse(list(seletiva_saidas_info), safe=False)

    except Exception as e:
        logger.exception("erro ao buscar dados de soltura seletiva.")
        return JsonResponse({'error': f'erro: {str(e)}'}, status=500)
