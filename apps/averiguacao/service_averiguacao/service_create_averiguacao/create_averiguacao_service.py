import logging
import traceback
from django.db import transaction
from apps.averiguacao.models import Averiguacao

def criar_averiguacao_service(data, arquivos):
    try:
        logging.info(f"Iniciando criação da averiguação com os dados: {data}")
        logging.info(f"Arquivos recebidos: {arquivos}")

        # Logs detalhados de chaves recebidas
        logging.info(f"Chaves em 'data': {list(data.keys())}")
        logging.info(f"Chaves em 'arquivos': {list(arquivos.keys())}")

        obrigatorios = ['tipo_servico', 'pa_da_averiguacao', 'data', 'hora_averiguacao', 'rota_averiguacao', 'imagem1', 'imagem4', 'averiguador']

        # Validação de campos obrigatórios
        for campo in obrigatorios:
            if campo.startswith('imagem'):
                # Logs mais detalhados para debug
                if campo in arquivos:
                    logging.info(f"Campo '{campo}' encontrado em arquivos. Tipo: {type(arquivos[campo])}")
                    logging.info(f"Valor de {campo}: {arquivos.get(campo)}")
                else:
                    logging.warning(f"Campo '{campo}' NÃO está presente em arquivos.")
                
                if campo not in arquivos or not arquivos[campo]:
                    logging.error(f'Campo obrigatório ausente ou vazio: {campo}')
                    raise ValueError(f'Campo obrigatório ausente: {campo}')
            else:
                if not data.get(campo):
                    logging.error(f'Campo obrigatório ausente: {campo}')
                    raise ValueError(f'Campo obrigatório ausente: {campo}')

        # Validação de rota
        rota_choices = dict(Averiguacao._meta.get_field('rota_averiguacao').choices)
        if data['rota_averiguacao'] not in rota_choices:
            logging.error('Rota averiguada inválida ou não encontrada.')
            raise ValueError('Rota averiguada inválida ou não encontrada.')

        # Prepara os dados da nova averiguação
        nova_averiguacao_data = {
            'tipo_servico': data['tipo_servico'],
            'pa_da_averiguacao': data['pa_da_averiguacao'],
            'data': data['data'],
            'hora_averiguacao': data['hora_averiguacao'],
            'rota_averiguacao': data['rota_averiguacao'],
            'averiguador': data['averiguador'],
        }

        # Adiciona imagens se existirem
        for i in range(1, 8):
            imagem_key = f'imagem{i}'
            if imagem_key in arquivos:
                nova_averiguacao_data[imagem_key] = arquivos[imagem_key]

        # Criação com segurança de transação
        with transaction.atomic():
            nova_averiguacao = Averiguacao.objects.create(**nova_averiguacao_data)

        logging.info(f"Averiguação criada com sucesso: {nova_averiguacao.id}")
        return nova_averiguacao

    except Exception as e:
        logging.error(f"Erro ao criar averiguação: {e}")
        logging.error(f"Detalhes do erro: {traceback.format_exc()}")
        raise e
