from ...models.models import Soltura
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def buscar_soltura_por_id(request, soltura_id):
    try:
        soltura = (
            Soltura.objects
            .select_related('motorista', 'veiculo')
            .prefetch_related('coletores')
            .only(
                'motorista__nome',
                'motorista__matricula',
                'tipo_equipe',
                'coletores',
                'data',
                'veiculo__prefixo',
                'veiculo__placa_veiculo',
                'frequencia',
                'setores',
                'celular',
                'lider',
                'hora_entrega_chave',
                'hora_saida_frota',
                'tipo_servico',
                'turno',
                'rota',
                'status_frota',
                'tipo_veiculo_selecionado',
            )
            .get(id=soltura_id)
        )

        resultado = {
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
            "tipo_veiculo_selecionado": soltura.tipo_veiculo_selecionado,
        }

        return JsonResponse(resultado, safe=False)

    except Soltura.DoesNotExist:
        logger.warning(f"Soltura com id {soltura_id} não encontrada.")
        return JsonResponse({"error": "Soltura não encontrada"}, status=404)

    except Exception as e:
        logger.error(f"Erro ao buscar soltura: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
