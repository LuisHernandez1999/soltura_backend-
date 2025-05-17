from django.utils.timezone import localdate
from django.db.models import Count
from apps.soltura.models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def contar_solturas_rsu_por_garagem():
    try:
        data_hoje = localdate()
        garages = ['PA1', 'PA2', 'PA3', 'PA4']
        solturas_por_garagem = (
            Soltura.objects
            .filter(data=data_hoje, tipo_servico='Rsu')
            .values('garagem')
            .annotate(total=Count('garagem'))
            .filter(garagem__in=garages)
        )
        resultado = {soltura['garagem']: soltura['total'] for soltura in solturas_por_garagem}
        for garagem in garages:
            resultado.setdefault(garagem, 0)
        total_solturas_hoje = Soltura.objects.filter(data=data_hoje, tipo_servico='Rsu').count()
        resultado['total'] = total_solturas_hoje

        logger.info("contagem de solturas Rsu por garagem realizada com sucesso: %s", resultado)
        return resultado

    except Exception as e:
        logger.exception("erro ao contar solturas por garagem")
        raise Exception(f"erro ao contar solturas: {str(e)}")
