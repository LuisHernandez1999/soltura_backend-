from django.db.models import Count
from ...models.models import Soltura
from django.utils.timezone import localdate
import logging

logger = logging.getLogger(__name__)

def distribuicao_status_por_data(tipo_servico='Remoção'):
    try:
        hoje = localdate.today()  # Pega a data de hoje, sem hora
        logger.info("Buscando distribuição de status para o tipo de serviço: %s, data: %s", tipo_servico, hoje)

        # Se o campo 'data_soltura' for um DateTimeField, use __date para comparar somente a data
        status_count = Soltura.objects.filter(data_soltura__date=hoje, tipo_servico=tipo_servico) \
            .values('status') \
            .annotate(qtd=Count('id'))
        
        # Criar o dicionário de status com suas respectivas quantidades
        status_dict = {status['status']: status['qtd'] for status in status_count}
        
        quantidade_em_andamento = status_dict.get('Em andamento', 0)
        quantidade_finalizado = status_dict.get('Finalizado', 0)

        logger.info("Distribuição de status: Em andamento - %d, Finalizado - %d", quantidade_em_andamento, quantidade_finalizado)

        return status_dict, quantidade_em_andamento, quantidade_finalizado

    except Exception as e:
        logger.error("Erro ao buscar distribuição de status: %s", str(e))
        raise Exception("Erro ao buscar distribuição de status")