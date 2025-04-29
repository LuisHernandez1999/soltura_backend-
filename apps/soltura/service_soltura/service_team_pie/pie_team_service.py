
from django.db.models import Count
from ...models.models import Soltura
from django.utils.timezone import now
import logging

logger = logging.getLogger(__name__)

def quantidade_solturas_por_equipe_dia():
    try:
        hoje = now().date()
        logger.info("Buscando quantidade de solturas por equipe para o dia: %s", hoje)

        
        solturas_por_equipe = Soltura.objects.filter(data=hoje) \
            .values('tipo_equipe') \
            .annotate(qtd=Count('id')) \
            .filter(tipo_equipe__in=['Equipe1(Matutino)', 'Equipe2(Vespertino)', 'Equipe3(Noturno)'])

        solturas_por_equipe_list = list(solturas_por_equipe)
        resultado = {equipe['tipo_equipe']: equipe['qtd'] for equipe in solturas_por_equipe_list}
        equipes = ['Equipe1(Matutino)', 'Equipe2(Vespertino)', 'Equipe3(Noturno)']
        for equipe in equipes:
            if equipe not in resultado:
                resultado[equipe] = 0

        logger.info("Distribuição de solturas por equipe: %s", resultado)
        return resultado
    except Exception as e:
        logger.error("Erro ao buscar quantidade de solturas por equipe: %s", str(e))
        raise Exception("Erro ao buscar quantidade de solturas por equipe")