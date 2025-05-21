from django.utils.timezone import localdate
from django.http import JsonResponse
from apps.soltura.models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def contar_solturas_seletiva_por_garagem(request):
    try:
        data_hoje = localdate()
        garages = ['PA1', 'PA2', 'PA3', 'PA4']
        resultado = {g: 0 for g in garages}
        solturas = Soltura.objects.filter(
            data=data_hoje,
            tipo_servico='Seletiva',
            garagem__in=garages
        )

        for s in solturas:
            garagem_formatada = str(s.garagem or '').strip().upper()
            if garagem_formatada in resultado:
                resultado[garagem_formatada] += 1
            else:
                logger.warning("Garagem ignorada: %s", garagem_formatada)

        resultado['total'] = solturas.count()

        return JsonResponse(resultado)

    except Exception as e:
        logger.exception("Erro ao contar solturas por garagem")
        return JsonResponse({'error': f'Erro ao contar solturas: {str(e)}'}, status=500)
