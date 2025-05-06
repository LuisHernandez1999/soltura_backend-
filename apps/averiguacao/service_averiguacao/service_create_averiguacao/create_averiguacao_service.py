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

   
        obrigatorios = ['hora_averiguacao', 'imagem1', 'imagem4', 'averiguador', 'garagem', 'rota']

      
        for campo in obrigatorios:
            if campo.startswith('imagem'):  
                if campo not in arquivos or not arquivos[campo]:
                    logging.error(f'Campo obrigatório ausente ou vazio: {campo}')
                    raise ValueError(f'Campo obrigatório ausente: {campo}')
            else:  # Dados
                if not data.get(campo):
                    logging.error(f'Campo obrigatório ausente: {campo}')
                    raise ValueError(f'Campo obrigatório ausente: {campo}')

        
        if 'soltura_ref' in data:
            try:
                soltura = Soltura.objects.get(pk=data['soltura_ref'], status_frota='Em Andamento')
            except Soltura.DoesNotExist:
                logging.error('Soltura informada não encontrada ou não está com status "Em Andamento".')
                raise ValueError('Soltura inválida.')
        else:
            soltura = None 

        garagem_valida = ['PA1', 'PA2', 'PA3', 'PA4']
        if data['garagem'] not in garagem_valida:
            logging.error(f'Valor de garagem inválido: {data["garagem"]}')
            raise ValueError('Garagem inválida.')

       
        if data['rota'] != 'AN21' and data['rota'] != 'AN24':  
            logging.error(f'Valor de rota inválido: {data["rota"]}')
            raise ValueError('Rota inválida.')
        nova_averiguacao_data = {
            'soltura_ref': soltura,
            'hora_averiguacao': data['hora_averiguacao'],
            'averiguador': data['averiguador'],
            'rota': data['rota'],  
            'garagem': data['garagem']  
        }

        for i in range(1, 8):
            imagem_key = f'imagem{i}'
            if imagem_key in arquivos:
                nova_averiguacao_data[imagem_key] = arquivos[imagem_key]

        
        with transaction.atomic():
            nova_averiguacao = Averiguacao.objects.create(**nova_averiguacao_data)

        logging.info(f"Averiguação criada com sucesso: {nova_averiguacao.id}")
        return nova_averiguacao

    except ValueError as e:
        logging.error(f"Erro de validação ao criar averiguação: {e}")
        raise e
    except Exception as e:
        logging.error(f"Erro ao criar averiguação: {e}")
        logging.error(f"Detalhes do erro: {traceback.format_exc()}")
        raise e