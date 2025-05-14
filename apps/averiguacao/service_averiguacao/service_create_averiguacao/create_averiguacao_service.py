import logging
import traceback
from django.db import transaction
from apps.averiguacao.models import Averiguacao
from apps.soltura.models.models import Soltura
from PIL import Image
from datetime import timedelta

def str_to_timedelta(time_str):
    if time_str:
        if len(time_str.split(':')) == 2:
            hours, minutes = map(int, time_str.split(':'))
            return timedelta(hours=hours, minutes=minutes)
        else:
            raise ValueError(f"Formato de tempo inválido: {time_str}. Esperado 'HH:MM'.")
    return None

MAX_IMAGE_SIZE_MB = 2 * 1024 * 1024  

def validar_imagem(imagem):
    try:
        img = Image.open(imagem)
        img.verify()  
    except (IOError, SyntaxError) as e:
        raise ValueError(f"O arquivo {imagem.name} não é uma imagem válida.")

def criar_averiguacao_service(data, arquivos): 
    try:
        logging.info(f"Iniciando criação da averiguação com os dados: {data}")
        logging.info(f"Arquivos recebidos: {arquivos}")
        logging.info(f"Chaves em 'data': {list(data.keys())}")
        logging.info(f"Chaves em 'arquivos': {list(arquivos.keys())}")

        if 'tipo_servico' not in data or not data['tipo_servico']:
            raise ValueError("Campo obrigatório ausente: tipo_servico")

        obrigatorios = [
            'hora_averiguacao', 'imagem1', 'imagem4', 'averiguador', 'garagem', 'rota', 'hora_inicio',
            'hora_encerramento', 'quantidade_viagens', 'velocidade_coleta', 'largura_rua', 'altura_fios',
            'caminhao_usado', 'equipamento_protecao', 'uniforme_completo', 'documentacao_veiculo',
            'inconformidades', 'acoes_corretivas', 'observacoes_operacao'
        ]

        imagens_validadas = {}

        for campo in obrigatorios:
            if campo.startswith('imagem'):
                if campo not in arquivos or not arquivos[campo]:
                    raise ValueError(f'Campo obrigatório ausente: {campo}')
                imagem = arquivos[campo]
                validar_imagem(imagem)
                if imagem.size > MAX_IMAGE_SIZE_MB:
                    raise ValueError(f'{campo} excede o tamanho máximo de 2MB.')
                imagens_validadas[campo] = imagem
            else:
                if not data.get(campo):
                    raise ValueError(f'Campo obrigatório ausente: {campo}')

        if 'hora_extras' in data and data['hora_extras'] == '':
            data['hora_extras'] = None  
        if 'horas_improdutivas' in data and data['horas_improdutivas'] == '':
            data['horas_improdutivas'] = None  

        soltura = None
        if 'soltura_ref' in data:
            try:
                soltura = Soltura.objects.get(pk=data['soltura_ref'], status_frota='Em Andamento')
            except Soltura.DoesNotExist:
                raise ValueError('Soltura inválida.')

        garagem_valida = ['PA1', 'PA2', 'PA3', 'PA4']
        if data['garagem'] not in garagem_valida:
            raise ValueError('Garagem inválida.')

        if data['rota'] not in ['AN21', 'AN24']:
            raise ValueError('Rota inválida.')

        def parse_bool(value):
            return str(value).strip().lower() in ['sim', 'true', '1']

        nova_averiguacao_data = {
            'soltura_ref': soltura,
            'tipo_servico': data['tipo_servico'],
            'hora_averiguacao': data['hora_averiguacao'],
            'averiguador': data['averiguador'],
            'rota': data['rota'],
            'garagem': data['garagem'],
            'coleta_com_puxada': parse_bool(data.get('coleta_com_puxada', False)),
            'puxada_adequada': parse_bool(data.get('puxada_adequada', True)),
            'quantidade_coletores': data.get('quantidade_coletores', 0),
            'hora_inicio': data.get('hora_inicio', '00:00'),
            'hora_encerramento': data.get('hora_encerramento', '00:00'),
            'hora_extras': str_to_timedelta(data.get('hora_extras', None)),
            'quantidade_viagens': data.get('quantidade_viagens', 0),
            'horas_improdutivas': str_to_timedelta(data.get('horas_improdutivas', None)),
            'velocidade_coleta': data.get('velocidade_coleta', 'Médio'),
            'largura_rua': data.get('largura_rua', 'Adequada'),
            'altura_fios': data.get('altura_fios', 'Adequada'),
            'caminhao_usado': data.get('caminhao_usado', 'Trucado'),
            'equipamento_protecao': data.get('equipamento_protecao', 'Conforme'),
            'uniforme_completo': data.get('uniforme_completo', 'Conforme'),
            'documentacao_veiculo': data.get('documentacao_veiculo', 'Conforme'),
            'inconformidades': data.get('inconformidades', ''),
            'acoes_corretivas': data.get('acoes_corretivas', ''),
            'observacoes_operacao': data.get('observacoes_operacao', ''),
        }

        for i in range(1, 8):
            imagem_key = f'imagem{i}'
            if imagem_key in arquivos and arquivos[imagem_key]:
                if imagem_key not in imagens_validadas:
                    imagem = arquivos[imagem_key]
                    validar_imagem(imagem)
                    if imagem.size > MAX_IMAGE_SIZE_MB:
                        raise ValueError(f'{imagem_key} excede o tamanho máximo de 2MB.')
                    imagens_validadas[imagem_key] = imagem
                nova_averiguacao_data[imagem_key] = imagens_validadas[imagem_key]

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
