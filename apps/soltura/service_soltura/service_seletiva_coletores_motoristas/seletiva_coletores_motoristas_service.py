from django.http import JsonResponse
from ...models.models import Soltura
import logging
from datetime import date

logger = logging.getLogger(__name__)

def contar_coletores_motorista_por_turno(request):  # <- Adiciona o 'request' aqui
    try:
        hoje = date.today()

        motorista_coletores_equipe1 = Soltura.objects.filter(
            tipo_equipe='Equipe1(Matutino)',
            data=hoje
        ).values('motorista', 'coletores').count()

        motorista_coletores_equipe2 = Soltura.objects.filter(
            tipo_equipe='Equipe2(Vespertino)',
            data=hoje
        ).values('motorista', 'coletores').count()

        motorista_coletores_equipe3 = Soltura.objects.filter(
            tipo_equipe='Equipe1(Noturno)',
            data=hoje
        ).values('motorista', 'coletores').count()

        resultado = {
            "Equipe1(Matutino)": motorista_coletores_equipe1,
            "Equipe2(Vespertino)": motorista_coletores_equipe2,
            "Equipe1(Noturno)": motorista_coletores_equipe3
        }

        logger.info("Contagem de coletores e motoristas por turno realizada com sucesso: %s", resultado)
        return JsonResponse(resultado)

    except Exception as e:
        logger.exception("Erro ao contar coletores e motoristas por turno")
        return JsonResponse(
            {"erro": f"Erro ao contar coletores e motoristas por turno: {str(e)}"},
            status=500
        )
