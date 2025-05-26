from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)


def buscar_soltura_por_id(soltura_id):
    try:
        logger.info(f"Buscando soltura com ID: {soltura_id}")

        soltura = (
            Soltura.objects
            .select_related('motorista', 'veiculo')
            .prefetch_related('coletores')
            .filter(id=soltura_id)
            .first()
        )

        if not soltura:
            logger.warning(f"soltura com ID {soltura_id} nao encontrada.")
            return None

        return {
            "motorista": soltura.motorista.nome if soltura.motorista else None,
            "matricula_motorista": soltura.motorista.matricula if soltura.motorista else None,
            "tipo_equipe": soltura.tipo_equipe,
            "coletores": [coletor.nome for coletor in soltura.coletores.all()],
            "data": soltura.data,
            "prefixo": soltura.veiculo.prefixo if soltura.veiculo else None,
            "frequencia": soltura.frequencia,
            "setores": soltura.setores,
            "garagem":soltura.garagem,
            "celular": soltura.celular,
            "lider": soltura.lider,
            "hora_entrega_chave": soltura.hora_entrega_chave.strftime('%H:%M:%S') if soltura.hora_entrega_chave else None,
            "hora_saida_frota": soltura.hora_saida_frota.strftime('%H:%M:%S') if soltura.hora_saida_frota else None,
            "hora_chegada": soltura.hora_chegada.strftime('%H:%M:%S') if soltura.hora_chegada else None,
            "tipo_servico": soltura.tipo_servico,
            "garagem":soltura.garagem,
            "hora_chegada":soltura.hora_chegada,
            "turno": soltura.turno,
            "rota": soltura.rota,
            "status_frota": soltura.status_frota,
            "tipo_veiculo_selecionado": soltura.tipo_veiculo,
            "bairro":soltura.bairro
        }
    except Exception as e:
        logger.error(f"erro ao buscar soltura por ID: {str(e)}")
        raise Exception(f"erro ao buscar soltura por ID: {str(e)}")
