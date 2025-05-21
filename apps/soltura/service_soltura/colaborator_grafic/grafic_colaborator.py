from django.http import JsonResponse
import logging
from django.utils.timezone import now
from ...models.models import Soltura
from django.utils import timezone

logger = logging.getLogger(__name__)
def contar_motoristas_e_coletores_hoje(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'O método deve ser GET.'}, status=405)

    try:
        hoje = timezone.localdate() 
        logger.debug(f"Data de hoje: {hoje}")
        total_motoristas = Soltura.objects.filter(data=hoje,tipo_servico='Remoção').values('motorista').count()
        logger.debug(f"Total de motoristas: {total_motoristas}")
        total_coletores = Soltura.objects.prefetch_related('coletores').filter(data=hoje,tipo_servico='Remoção').values('coletores').count()
        logger.debug(f"Total de coletores: {total_coletores}")

        total_geral = total_motoristas + total_coletores
        logger.debug(f"Total geral: {total_geral}")

        return JsonResponse({
            'total_motoristas': total_motoristas,
            'total_coletores': total_coletores,
            'total_geral': total_geral
        }, status=200)

    except Exception as e:
        logger.error(f"Erro ao contar motoristas e coletores: {e}")
        return JsonResponse({'error': f'Erro ao contar motoristas e coletores: {str(e)}'}, status=500)
