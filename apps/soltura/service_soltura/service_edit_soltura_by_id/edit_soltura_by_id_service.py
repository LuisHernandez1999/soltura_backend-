from django.shortcuts import get_object_or_404
from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def editar_soltura_por_id(soltura_id: int, dados: dict) -> Soltura:
    soltura = get_object_or_404(Soltura, pk=soltura_id)
    
    campos_permitidos = [
        'tipo_equipe', 'turno', 'status_frota','motorista','coletores','garagem',
        'hora_entrega_chave', 'hora_saida', 'hora_chegada', 'frequencia',
        'setor', 'celular', 'lider', 'rota', 'tipo_veiculo_selecionada', 'veiculo'
    ]

    for campo in campos_permitidos:
        if campo in dados:
            setattr(soltura, campo, dados[campo])

    soltura.save()
    logger.info(f"soltura {soltura_id} atualizada com sucesso.")
    return soltura
