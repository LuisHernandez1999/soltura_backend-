from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def deletar_soltura(soltura_id):
    try:
        soltura = Soltura.objects.get(id=soltura_id)
        soltura.averiguacoes.all().delete()
        soltura.delete()
        logger.info(f"soltura com id {soltura_id} deletada com sucesso.")
        return {"mensagem": "soltura deletada com sucesso."}, 200

    except Soltura.DoesNotExist:
        logger.warning(f"soltura com id {soltura_id} nao encontrada para exclusão.")
        return {"error": "soltura nao encontrada"}, 404
    except Exception as e:
        logger.error(f"erro ao deletar soltura: {str(e)}")
        return {"error": str(e)}, 500
