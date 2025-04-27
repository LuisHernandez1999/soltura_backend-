import logging
from datetime import datetime
from django.utils import timezone
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo
from ...models.models import Soltura

logger = logging.getLogger(__name__)

def converter_para_data_hora(valor):
    formatos = [
        '%H:%M', '%H:%M:%S', '%d/%m/%Y %H:%M',
        '%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ',
    ]
    for formato in formatos:
        try:
            dt = datetime.strptime(valor, formato)
            if dt.year < 2025:
                raise ValueError(f"Data anterior a 2025 não é válida: {valor}")
            if formato in ['%H:%M', '%H:%M:%S']:
                raise ValueError(f"Formato de hora sem data completa: {valor}")
            return timezone.make_aware(dt, timezone.get_default_timezone())
        except ValueError:
            continue
    raise ValueError(f"Formato de data/hora inválido ou data anterior a 2025: {valor}")


def editar_soltura(soltura_id, data):
    tipo_servico = data.get('tipo_servico', '').lower()
    required_fields = {'motorista', 'veiculo', 'frequencia', 'setor', 'hora_entrega_chave', 'hora_saida_frota', 'turno', 'tipo_servico'}

    if tipo_servico != 'varrição':
        required_fields.add('coletores')

    missing_fields = required_fields - data.keys()
    if missing_fields:
        return {'error': 'Campos obrigatórios faltando', 'missing_fields': list(missing_fields)}, 400

    soltura = Soltura.objects.filter(id=soltura_id).first()
    if not soltura:
        return {'error': 'soltura nao encontrada'}, 404

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
        return {'error': 'motorista ou veiculo nao encontrado ou inativo'}, 404

    coletores = []
    if tipo_servico != 'varrição':
        coletores = list(Colaborador.objects.filter(
            nome__in=data['coletores'],
            funcao="Coletor",
            status="ATIVO"
        )[:3])

        if not coletores:
            return {'error': 'coletores nao encontrados ou inativos'}, 404

    hora_entrega_chave = converter_para_data_hora(data['hora_entrega_chave'])
    hora_saida_frota = converter_para_data_hora(data['hora_saida_frota'])
    hora_chegada_raw = data.get('hora_chegada')
    hora_chegada = converter_para_data_hora(hora_chegada_raw) if hora_chegada_raw else None

    # Atualiza a soltura
    soltura.motorista = motorista
    soltura.veiculo = veiculo
    soltura.tipo_equipe = data['tipo_equipe']
    soltura.frequencia = data['frequencia']
    soltura.setores = data['setor']
    soltura.celular = data.get('celular', '')
    soltura.lider = data.get('lider', '')
    soltura.hora_entrega_chave = hora_entrega_chave
    soltura.hora_saida_frota = hora_saida_frota
    soltura.turno = data['turno']
    soltura.hora_chegada = hora_chegada
    soltura.tipo_servico = data['tipo_servico']
    soltura.rota = data.get('rota') or None
    soltura.data = data.get('data')
    soltura.status_frota = data.get('status_frota')
    soltura.tipo_veiculo_selecionado=data('')

    if coletores:
        soltura.coletores.set(coletores)

    soltura.save()

    return soltura, coletores, veiculo
