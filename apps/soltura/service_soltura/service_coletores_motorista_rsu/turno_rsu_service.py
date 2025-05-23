from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils.timezone import localdate
from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)

@require_GET
def quantidade_motorista_coletores_equipe(request):
    try:
        hoje = localdate()
        logger.info("buscando quantidade de motoristas e coletores por equipe no dia: %s", hoje)

        equipes = ['Equipe(Diurno)', 'Equipe(Notunro)']
        resultado = {}

        for equipe in equipes:
            solturas = Soltura.objects.filter(data=hoje, tipo_equipe=equipe,tipo_servico='Rsu')
            qtd_motoristas = solturas.values('motorista').count()
            qtd_coletores = solturas.values('coletores').count()
            resultado[equipe] = {
                'motoristas': qtd_motoristas,
                'coletores': qtd_coletores
            }

        logger.info("distribuicao por equipe: %s", resultado)
        return JsonResponse(resultado)  

    except Exception as e:
        logger.error("erro ao buscar quantidade de motoristas/coletores por equipe: %s", str(e))
        return JsonResponse(
            {"error": "erro ao buscar quantidade por equipe", "details": str(e)},
            status=500
        )
