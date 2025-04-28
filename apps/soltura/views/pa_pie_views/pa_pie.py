from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.models import Soltura
from django.utils.timezone import localdate
from django.db.models import Count

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localdate
from django.db.models import Count
from ...models.models import Soltura

@csrf_exempt
def quantidade_soltura_equipes_dia(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'O método deve ser GET'}, status=400)
    
    try:
        hoje = localdate()  # Corrige para pegar a data correta de hoje

        # Certifique-se de usar o campo correto, no caso, 'data' em vez de 'data_soltura'
        solturas_por_equipe = Soltura.objects.filter(data=hoje) \
            .values('tipo_equipe') \
            .annotate(qtd=Count('id')) \
            .filter(tipo_equipe__in=['Equipe1(Matutino)', 'Equipe2(Vespertino)', 'Equipe3(Noturno)'])

        # Criar o dicionário de resultados com a quantidade de solturas por tipo de equipe
        resultado = {equipe['tipo_equipe']: equipe['qtd'] for equipe in solturas_por_equipe}

        # Definir as equipes com valor 0 caso não exista soltura para algum tipo de equipe
        equipes = ['Equipe1(Matutino)', 'Equipe2(Vespertino)', 'Equipe3(Noturno)']
        for equipe in equipes:
            resultado.setdefault(equipe, 0)

        return JsonResponse(resultado)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
