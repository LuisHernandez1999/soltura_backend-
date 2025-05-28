import logging
from apps.equipamentos.models import Equipamento

logger = logging.getLogger(__name__)

def editar_equipamento(id_equipamento, prefixo, implemento, status):
    try:
        equipamento_pra_editar = Equipamento.objects.get(id=id_equipamento)
        equipamento_pra_editar.prefixo_equipamento = prefixo
        equipamento_pra_editar.implemento = implemento
        equipamento_pra_editar.status_equipamento = status
        equipamento_pra_editar.save()
        logger.info(f"equipamento com ID {id_equipamento} atualizado com sucesso.")
    except Equipamento.DoesNotExist:
        logger.warning(f"equipamento com ID {id_equipamento} nao encontrado.")
    except Exception as e:
        logger.error(f"erro ao editar equipamento: {e}")
