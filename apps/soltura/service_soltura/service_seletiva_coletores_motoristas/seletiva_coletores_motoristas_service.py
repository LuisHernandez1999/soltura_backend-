from django.http import JsonResponse
from ...models.models import Soltura
import logging
from datetime import date

logger = logging.getLogger(__name__)

def contar_coletores_motorista_por_turno(request):
    try:
        hoje = date.today()
        resultado = {}

        equipes = {
            "Equipe1(Matutino)": "Equipe1(Matutino)",
            "Equipe2(Vespertino)": "Equipe2(Vespertino)",
            "Equipe3(Noturno)": "Equipe3(Noturno)"
        }

        for nome_equipe, tipo_equipe in equipes.items():
            solturas = Soltura.objects.filter(tipo_equipe=tipo_equipe, data=hoje)
            motoristas = solturas.values_list('motorista', flat=True).exclude(motorista__isnull=True)
            num_motoristas = motoristas.count()
            num_coletores = 0
            for soltura in solturas:
                num_coletores += soltura.coletores.count()

            resultado[nome_equipe] = {
                "motoristas": num_motoristas,
                "coletores": num_coletores
            }

        logger.info("Contagem de coletores e motoristas por turno realizada com sucesso: %s", resultado)
        return JsonResponse(resultado)

    except Exception as e:
        logger.exception("Erro ao contar coletores e motoristas por turno")
        return JsonResponse(
            {"erro": f"Erro ao contar coletores e motoristas por turno: {str(e)}"},
            status=500
        )
