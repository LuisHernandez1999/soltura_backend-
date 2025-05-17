from django.db.models import Count
from ...models.models import Soltura
from django.utils.timezone import localdate
import logging

logger = logging.getLogger(__name__)

def quantidade_motorista_coletores_equipe():
    try:
        hoje = localdate()
        logger.info("buscando quantidade de motoristas e coletores por equipe no dia: %s", hoje)

        equipes = ['Equipe1(Matutino)', 'Equipe2(Vespertino)', 'Equipe3(Noturno)']
        resultado = {}

        for equipe in equipes:
            solturas = Soltura.objects.filter(data=hoje, tipo_equipe=equipe,)
            qtd_motoristas = solturas.values('motorista').distinct().count()
            qtd_coletores = solturas.values('coletores').distinct().count()
            resultado[equipe] = {
                'motoristas': qtd_motoristas,
                'coletores': qtd_coletores
            }

        logger.info("distribuicao por equipe: %s", resultado)
        return resultado

    except Exception as e:
        logger.error("erro ao buscar quantidade de motoristas/coletores por equipe: %s", str(e))
        raise Exception("erro ao buscar quantidade por equipe: " + str(e))
