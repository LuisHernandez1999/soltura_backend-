from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def buscar_solturas_rsu(request):
    try:
        solturas = (
            Soltura.objects
            .filter(tipo_servico='Rsu')
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
        )

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
                "tipo_veiculo_selecionado": soltura.tipo_veiculo_selecionado,
            })

        logger.info("encontradas %d solturas", len(resultados))
        from django.http import JsonResponse
        return JsonResponse({"solturas": resultados}, safe=False)

    except Exception as e:
        logger.error(f"erro ao buscar solturas: {str(e)}")
        from django.http import JsonResponse
        return JsonResponse({"error": str(e)}, status=500)