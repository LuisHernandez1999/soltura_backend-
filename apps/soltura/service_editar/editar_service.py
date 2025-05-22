# services/soltura_service.py
from django.shortcuts import get_object_or_404
from ..models.models import Soltura
import logging

logger = logging.getLogger(__name__)
def editar_soltura(id: int, dados: dict) -> Soltura:
    soltura = get_object_or_404(Soltura, pk=id)
    campos_permitidos = [
        'tipo_equipe', 'turno', 'status_frota','motorista','coletores','garagem'
        'hora_entrega_chave', 'hora_saida_frota','hora_chegada', 'frequencia',
        'setores', 'celular', 'lider', 'rota', 'tipo_veiculo_selecionado'
    ]
    for campo in campos_permitidos:
        if campo in dados:
            setattr(soltura, campo, dados[campo])
    soltura.save()
    logger.info(f"soltura {id} atualizada com sucesso.")
    return soltura
