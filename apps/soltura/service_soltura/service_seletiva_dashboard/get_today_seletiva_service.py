from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.timezone import localdate
from django.views.decorators.cache import cache_page
from apps.soltura.models.models import Soltura
import logging

logger = logging.getLogger(__name__)

@cache_page(60 * 4)  # cache por 4 minutos
def dashboard_seletiva_dados_hoje(request):
    try:
        data_hoje = localdate()
        garages = ['PA1', 'PA2', 'PA3', 'PA4']

        # Query otimizada para seletivas com contagens
        seletivas = (
            Soltura.objects.filter(data=data_hoje, tipo_servico='Seletiva', garagem__in=garages)
            .values('garagem', 'turno')
            .annotate(
                motoristas_count=Count('motorista'),
                veiculos_count=Count('veiculo'),
                coletores_count=Count('coletores')
            )
        )

        seletiva_por_pa = {g: {'turnos': set(), 'motoristas': 0, 'veiculos': 0, 'coletores': 0} for g in garages}
        total_seletivas = 0

        for entry in seletivas:
            g = entry['garagem']
            seletiva_por_pa[g]['turnos'].add(entry['turno'])
            seletiva_por_pa[g]['motoristas'] += entry['motoristas_count']
            seletiva_por_pa[g]['veiculos'] += entry['veiculos_count']
            seletiva_por_pa[g]['coletores'] += entry['coletores_count']
            total_seletivas += 1

        for g in garages:
            seletiva_por_pa[g]['turnos'] = list(seletiva_por_pa[g]['turnos'])

        # Equipes por turno - sem prefetch_related
        equipes = {
            "Equipe(Diurno)": "Equipe(Diurno)",
            "Equipe(Noturno)": "Equipe(Noturno)"
        }

        por_turno = {}
        for nome_equipe, tipo_equipe in equipes.items():
            base_queryset = Soltura.objects.filter(tipo_equipe=tipo_equipe, data=data_hoje)

            motoristas = (
                base_queryset
                .values_list('motorista', flat=True)
                .exclude(motorista__isnull=True)
                .distinct()
                .count()
            )

            coletores = (
                base_queryset
                .values('coletores')
                .distinct()
                .count()
            )

            por_turno[nome_equipe] = {
                "motoristas": motoristas,
                "coletores": coletores,
            }

        # Quantidade seletiva por garagem
        seletivas_totais = (
            Soltura.objects.filter(data=data_hoje, tipo_servico='Seletiva', garagem__in=garages)
            .values('garagem')
            .annotate(count=Count('id'))
        )
        quantidade_seletiva_por_garagem = {g: 0 for g in garages}
        total = 0
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
