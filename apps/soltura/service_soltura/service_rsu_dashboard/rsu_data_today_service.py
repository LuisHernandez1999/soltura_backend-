from django.db.models import Count
from django.http import JsonResponse
from django.utils.timezone import localdate
from django.views.decorators.http import require_GET
from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)

@require_GET
def dados_rsu_hoje(request):
    try:
        hoje = localdate()

        def contar_por_garagem(nome_garagem):
            queryset = Soltura.objects.filter(garagem=nome_garagem, data=hoje, tipo_servico='Rsu')
            return {
                'turnos': list(queryset.values_list('turno', flat=True)),
                'motoristas': queryset.values('motorista').count(),
                'veiculos': queryset.values('veiculo').count(),
                'coletores': queryset.filter(coletores__isnull=False).values('coletores').count()
            }


        contagem_pa = {
            'PA1': contar_por_garagem('PA1'),
            'PA2': contar_por_garagem('PA2'),
            'PA3': contar_por_garagem('PA3'),
            'PA4': contar_por_garagem('PA4'),
        }


        equipes = ['Equipe(Diurno)', 'Equipe(Noturno)']
        contagem_equipes = {}
        for equipe in equipes:
            solturas = Soltura.objects.filter(data=hoje, tipo_equipe=equipe, tipo_servico='Rsu')
            qtd_motoristas = solturas.values('motorista').count()
            qtd_coletores = solturas.values('coletores').count()
            contagem_equipes[equipe] = {
                'motoristas': qtd_motoristas,
                'coletores': qtd_coletores
            }


        total_rsu_hoje = Soltura.objects.filter(tipo_servico__iexact='Rsu', data=hoje) \
                                         .values('motorista', 'veiculo') \
                                         .count()
        resultado = {
            'contagem_geral_por_pa_rsu': contagem_pa,
            'quantidade_motorista_coletores_equipe': contagem_equipes,
            'total_rsu_realizadas_hoje': {'total_rsu_hoje': total_rsu_hoje}
        }
        return JsonResponse(resultado)
    except Exception as e:
        logger.error(f"Erro ao buscar resumo RSU: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
