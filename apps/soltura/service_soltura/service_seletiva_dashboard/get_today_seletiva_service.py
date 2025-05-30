from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.timezone import localdate
from apps.soltura.models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def dashboard_seletiva_dados_hoje(request):
    try:
        data_hoje = localdate()
        garages = ['PA1', 'PA2', 'PA3', 'PA4']
        seletivas = (
            Soltura.objects.filter(data=data_hoje, tipo_servico='Seletiva', garagem__in=garages)
            .prefetch_related('coletores') 
            .values('garagem', 'turno')
            .annotate(
                motoristas_count=Count('motorista', distinct=True),
                veiculos_count=Count('veiculo', distinct=True),
                coletores_count=Count('coletores', distinct=True)
            )
        )

        # Montar resultado seletiva_por_pa
        seletiva_por_pa = {g: {'turnos': set(), 'motoristas': 0, 'veiculos': 0, 'coletores': 0} for g in garages}
        total_seletivas = 0

        for entry in seletivas:
            g = entry['garagem']
            seletiva_por_pa[g]['turnos'].add(entry['turno'])
            seletiva_por_pa[g]['motoristas'] += entry['motoristas_count']
            seletiva_por_pa[g]['veiculos'] += entry['veiculos_count']
            seletiva_por_pa[g]['coletores'] += entry['coletores_count']
            total_seletivas += 1

        # Converte set para lista em 'turnos'
        for g in garages:
            seletiva_por_pa[g]['turnos'] = list(seletiva_por_pa[g]['turnos'])

        # Agora query para equipes por turno, usando filtro por tipo_equipe
        equipes = {
            "Equipe(Diurno)": "Equipe(Diurno)",
            "Equipe(Noturno)": "Equipe(Noturno)"
        }

        por_turno = {}
        for nome_equipe, tipo_equipe in equipes.items():
            solturas = (
                Soltura.objects.filter(tipo_equipe=tipo_equipe, data=data_hoje)
                .prefetch_related('coletores')
            )
            motoristas = solturas.values_list('motorista', flat=True).exclude(motorista__isnull=True).distinct().count()
            # soma coletores com agregação direta (evitar loop)
            coletores = (
                Soltura.objects.filter(tipo_equipe=tipo_equipe, data=data_hoje, coletores__isnull=False)
                .distinct()
                .aggregate(total_coletores=Count('coletores'))
            )['total_coletores'] or 0

            por_turno[nome_equipe] = {
                "motoristas": motoristas,
                "coletores": coletores,
            }

        # Quantidade seletivas por garagem simplificada (já temos seletiva_por_pa mas somar contagem direta)
        quantidade_seletiva_por_garagem = {g: 0 for g in garages}
        total = 0
        seletivas_totais = (
            Soltura.objects.filter(data=data_hoje, tipo_servico='Seletiva', garagem__in=garages)
            .values('garagem')
            .annotate(count=Count('id'))
        )
        for s in seletivas_totais:
            g = s['garagem']
            quantidade_seletiva_por_garagem[g] = s['count']
            total += s['count']
        quantidade_seletiva_por_garagem['total'] = total

        resultado = {
            'seletiva_por_pa': seletiva_por_pa,
            'por_turno': por_turno,
            'quantidade_seletiva_por_garagem': quantidade_seletiva_por_garagem,
            'total_seletivas_hoje': total,
        }

        logger.info("Dashboard solturas geral calculado com sucesso")
        return JsonResponse(resultado)

    except Exception as e:
        logger.error(f"Erro no dashboard_solturas_geral: {str(e)}", exc_info=True)
        return JsonResponse({'erro': str(e)}, status=500)
