from django.http import JsonResponse
from apps.soltura.models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def retornar_infos_seletiva(request):
    try:
        solturas = (
            Soltura.objects
            .filter(tipo_servico__iexact='Seletiva')
            .select_related('motorista', 'veiculo')  
            .prefetch_related('coletores')
        )

        resultado = []
        for s in solturas:
            resultado.append({
                'motorista': s.motorista.nome if s.motorista else None,
                'hora_saida_frota': s.hora_saida_frota,
                "prefixo": s.veiculo.prefixo if s.veiculo else None,
                'hora_entrega_chave': s.hora_entrega_chave,
                'hora_chegada': s.hora_chegada,
                'coletores': [c.nome for c in s.coletores.all()],
                'data': s.data.isoformat() if s.data else None,
                'lider': s.lider,
                'rota': s.rota,
                'tipo_equipe': s.tipo_equipe,
                'status_frota': s.status_frota,
                'tipo_veiculo_selecionado': s.tipo_veiculo_selecionado,
            })

        return JsonResponse(resultado, safe=False)

    except Exception as e:
        logger.exception("Erro ao buscar dados de soltura seletiva.")
        return JsonResponse({'error': f'erro: {str(e)}'}, status=500)
