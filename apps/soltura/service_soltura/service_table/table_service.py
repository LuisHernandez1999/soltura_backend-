# services/soltura_service.py
from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def buscar_solturas(placa=None):
    try:
        logger.info("Buscando solturas com filtro de placa: %s", placa)

        solturas = (
            Soltura.objects
            .select_related('motorista', 'veiculo')
            .prefetch_related('coletores')
            .order_by('-hora_saida_frota')
            .filter(tipo_servico='Remoção')
        )

        if placa:
            solturas = solturas.filter(veiculo__placa_veiculo=placa)

        resultados = []
        for soltura in solturas:
            resultados.append({
                "motorista": soltura.motorista.nome if soltura.motorista else None,
                "matricula_motorista": soltura.motorista.matricula if soltura.motorista else None,
                "tipo_equipe": soltura.tipo_equipe,
                "coletores": [coletor.nome for coletor in soltura.coletores.all()],
                "data": soltura.data,
                "prefixo": soltura.veiculo.prefixo if soltura.veiculo else None,
                "frequencia": soltura.frequencia,
                "setores": soltura.setores,
                "celular": soltura.celular,
                "lider": soltura.lider,
                "hora_entrega_chave": soltura.hora_entrega_chave.strftime('%H:%M:%S') if soltura.hora_entrega_chave else None,
                "hora_saida_frota": soltura.hora_saida_frota.strftime('%H:%M:%S') if soltura.hora_saida_frota else None,
                "tipo_servico": soltura.tipo_servico,
                "turno": soltura.turno,
                "rota": soltura.rota,
                "status_frota": soltura.status_frota,
                "tipo_veiculo_selecionado": soltura.tipo_veiculo,
            })

        logger.info("Encontradas %d solturas", len(resultados))
        return resultados

    except Exception as e:
        logger.error(f"Erro ao buscar solturas: {str(e)}")
        raise Exception(f"Erro ao buscar solturas: {str(e)}")