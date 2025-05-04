import logging
import traceback
from django.db import transaction
from apps.averiguacao.models import Averiguacao
from apps.soltura.models.models import Soltura

def criar_averiguacao_service(data, arquivos):
    try:
        logging.info(f"Iniciando criação da averiguação com os dados: {data}")
        logging.info(f"Arquivos recebidos: {arquivos}")
        logging.info(f"Chaves em 'data': {list(data.keys())}")
        logging.info(f"Chaves em 'arquivos': {list(arquivos.keys())}")

        obrigatorios = ['soltura_ref', 'hora_averiguacao', 'imagem1', 'imagem4', 'averiguador']

        for campo in obrigatorios:
            if campo.startswith('imagem'):
                if campo not in arquivos or not arquivos[campo]:
                    logging.error(f'Campo obrigatório ausente ou vazio: {campo}')
                    raise ValueError(f'Campo obrigatório ausente: {campo}')
            else:
                if not data.get(campo):
                    logging.error(f'Campo obrigatório ausente: {campo}')
                    raise ValueError(f'Campo obrigatório ausente: {campo}')

        try:
            soltura = Soltura.objects.get(pk=data['soltura_ref'], status_frota='Em Andamento')
        except Soltura.DoesNotExist:
            logging.error('Soltura informada não encontrada ou não está com status "Em Andamento".')
            raise ValueError('Soltura inválida.')

        nova_averiguacao_data = {
            'soltura_ref': soltura,
            'hora_averiguacao': data['hora_averiguacao'],
            'averiguador': data['averiguador'],
        }
        for i in range(1, 8):
            imagem_key = f'imagem{i}'
            if imagem_key in arquivos:
                nova_averiguacao_data[imagem_key] = arquivos[imagem_key]

        with transaction.atomic():
            nova_averiguacao = Averiguacao.objects.create(**nova_averiguacao_data)

        logging.info(f"Averiguação criada com sucesso: {nova_averiguacao.id}")
        return nova_averiguacao

    except Exception as e:
        logging.error(f"Erro ao criar averiguação: {e}")
        logging.error(f"Detalhes do erro: {traceback.format_exc()}")
        raise e
