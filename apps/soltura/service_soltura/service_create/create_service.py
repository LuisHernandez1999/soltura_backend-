import logging
from datetime import datetime
from django.utils import timezone
from ...models.models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo

logger = logging.getLogger(__name__)

def converter_para_data_hora(valor):
    if valor is None:
        raise ValueError("O valor de hora não pode ser None.")
    if not isinstance(valor, str):
        raise ValueError("O valor de hora deve ser uma string.")
    
    formato = "%Y-%m-%d %H:%M:%S"  # Ajuste o formato conforme necessário
    return datetime.strptime(valor, formato)


def cadastrar_soltura_service(data):
    tipo_servico = data.get('tipo_servico', '').lower()

    required_fields = {
        'motorista', 'veiculo', 'frequencia', 
        'hora_entrega_chave', 'hora_saida_frota', 'turno', 'tipo_servico','tipo_equipe','status_frota'
    }
    if tipo_servico != 'varrição':
        required_fields.add('coletores')

    missing_fields = required_fields - data.keys()
    if missing_fields:
        logger.warning(f"campos obrigatorios faltando: {missing_fields}")
        raise ValueError(f"campos obrigatorios faltando: {missing_fields}")

    motorista = Colaborador.objects.filter(
        nome=data['motorista'],
        funcao="Motorista",
        status__in=["ATIVO", "Ativo"]
    ).first()

    prefixo = data.get('veiculo') or data.get('prefixo')
    veiculo = Veiculo.objects.filter(
        prefixo=prefixo,
        status__in=["ATIVO", "Ativo"]
    ).first()

    if not motorista or not veiculo:
        logger.warning("motorista ou veículo nao encontrado ou inativo.")
        raise ValueError('motorista ou veiculo nao encontrado ou inativo')

    coletores = []
    if tipo_servico != 'varrição':
        coletores = list(Colaborador.objects.filter(
            nome__in=data['coletores'],
            funcao="Coletor",
            status="ATIVO"
        )[:3])

        if not coletores:
            logger.warning("coletores nao encontrados ou inativos.")
            raise ValueError('coletores nao encontrados ou inativos')

    hora_entrega_chave = converter_para_data_hora(data['hora_entrega_chave'])
    hora_saida_frota = converter_para_data_hora(data['hora_saida_frota'])
    hora_chegada_raw = data.get('hora_chegada')
    hora_chegada = converter_para_data_hora(hora_chegada_raw) if hora_chegada_raw else None 

    data_saida = hora_saida_frota.date()
    soltura_duplicada = Soltura.objects.filter(
        motorista=motorista,
        data=data_saida,
        hora_saida_frota=hora_saida_frota
    ).exists()

    if soltura_duplicada:
        logger.warning(f"duplicacao de soltura detectada para motorista {motorista.nome} em {hora_saida_frota}")
        raise ValueError('ja existe um cadastro com esse motorista e essa hora de saida hoje.')

    soltura = Soltura.objects.create(
        motorista=motorista,
        veiculo=veiculo,
        data=data['data'],
        tipo_equipe=data['tipo_equipe'],
        frequencia=data['frequencia'],
        garagem=data['garagem'],
        celular=data.get('celular', ''),
        lider=data.get('lider', ''),
        hora_entrega_chave=hora_entrega_chave,
        hora_saida_frota=hora_saida_frota,
        turno=data['turno'],
        hora_chegada=hora_chegada,
        tipo_servico=data['tipo_servico'],
        rota=data.get('rota') or None,
        status_frota=data.get('status_frota'),
        tipo_veiculo_selecionado=data('tipo_veiculo_selecionado')
    )

    if coletores:
        soltura.coletores.set(coletores)

    return soltura, veiculo, coletores, motorista, hora_entrega_chave, hora_saida_frota, hora_chegada