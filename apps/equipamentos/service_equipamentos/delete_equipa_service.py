import logging
from apps.equipamentos.models import Equipamento

logger = logging.getLogger(__name__)

def deletar_equipamento(id_equipamento):
    try:
        Equipamento.objects.filter(id=id_equipamento).delete()
        logger.info(f"equipamento com ID {id_equipamento} deletado com sucesso.")
    except Exception as e:
        logger.error(f"erro ao deletar equipamento: {e}")
