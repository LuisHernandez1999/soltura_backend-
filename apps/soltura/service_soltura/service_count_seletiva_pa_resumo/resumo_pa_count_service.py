from django.db.models import Count
from django.http import JsonResponse
from django.utils.timezone import localdate
from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def contagem_geral_por_pa_seltiva(request):
    try:
        data_hoje = localdate()

        def contar_por_garagem(nome_garagem):
            queryset = Soltura.objects.filter(garagem=nome_garagem, data=data_hoje,tipo_servico='Seletiva')
            return {
                'turnos': list(queryset.values_list('turno', flat=True)),
                'motoristas': queryset.values('motorista').count(),
                'veiculos': queryset.values('veiculo').count(),
                'coletores': queryset.filter(coletores__isnull=False)
                                      .values('coletores').count()
            }
        resultado = {
            'PA1': contar_por_garagem('PA1'),
            'PA2': contar_por_garagem('PA2'),
            'PA3': contar_por_garagem('PA3'),
            'PA4': contar_por_garagem('PA4'),
        }
        return JsonResponse(resultado)
    except Exception as e:
        logger.error(f"erro ao contar por PA: {str(e)}")
        return JsonResponse({'erro': str(e)}, status=500)
