from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def buscar_soltura_por_id(request, soltura_id):
    try:
        soltura_editar = Soltura.objects.select_related('motorista').select_related('veiculo').prefetch_related('coletores').only( 'coletores',
            'hora_entrega_chave',
            'hora_saida',
            'hora_chegada',
            'status_frota',
            'bairro',
            'rota',
            'garagem',
            'tipo_veiculo_selecionada',
            'tipo_servico',
            'lider',
            'celular',).get(id=soltura_id)
        return soltura_editar
    except:
        raise ValueError('soltura {soltura_id} não encontrada')
    
    