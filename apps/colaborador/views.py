from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json
from .models import Colaborador

TURNO = ['Diurno', 'Noturno', 'Vespertino']
TIPO_FUNCAO = ["Motorista", "Coletor", "Operador"]
TIPOS_PA = ["PA1", "PA2", "PA3", "PA4"]
STATUS = ["ATIVO", "INATIVO"]

@csrf_exempt
@require_POST


def criar_colaborador(request):
    try:
        data = json.loads(request.body)
        nome = data.get("nome", "").strip()
        matricula = str(data.get("matricula", "")).strip()
        funcao = data.get("funcao", "").strip()
        turno = data.get("turno", "").strip()
        status = data.get("status", "").strip()
        pa = data.get("pa", "").strip()

        if (
            not nome or
            not matricula or
            funcao not in Colaborador.TIPOS_FUNCAO or
            turno not in Colaborador.TIPOS_TURNO or
            status not in Colaborador.TIPOS_STATUS or
            pa not in Colaborador.TIPOS_PA
        ):
            return JsonResponse({"error": "dados invalidos"}, status=400)

        if Colaborador.objects.filter(matricula=matricula).exists():
            return JsonResponse({"error": "matricula ja cadastrada"}, status=400)

        colaborador = Colaborador.objects.create(
            nome=nome,
            matricula=matricula,
            funcao=funcao,
            turno=turno,
            status=status,
            pa=pa
        )

        return JsonResponse({"message": "colaborador criado com sucesso", "id": colaborador.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "formato JSON invalido"}, status=400)
    except IntegrityError:
        return JsonResponse({"error": "erro ao salvar no banco de dados"}, status=500)



@require_GET
def colaboradores_lista_motoristas_ativos(request):
    colaboradores = Colaborador.objects.filter(status="ATIVO", funcao="Motorista") \
        .values_list("nome", "matricula", named=True)
    
    return JsonResponse(
        {"colaboradores_lista": [{"nome": colab.nome, "matricula": colab.matricula} for colab in colaboradores]}
    )


@require_GET
def colaboradores_lista_coletores(request):
    colaboradores = Colaborador.objects.filter(status="ATIVO", funcao="Coletor").values("nome", "matricula").distinct()
    colaboradores_info = [{"nome": colab["nome"], "matricula": colab["matricula"]} for colab in colaboradores]
    return JsonResponse({
        "colaboradores_lista": colaboradores_info,
    }, json_dumps_params={'ensure_ascii': False})

def contar_colaboradores_por_funcao(funcao):
    return Colaborador.objects.filter(status="ATIVO", funcao=funcao).count()

@require_GET
def colaboradores_quantidade_motoristas(request):
    quantidade_motoristas = Colaborador.objects.filter(status="ATIVO", funcao="Motorista").count()
    return JsonResponse({"quantidade_motoristas": quantidade_motoristas})

@require_GET
def colaboradores_quantidade_coletores(request):
    quantidade_coletores = contar_colaboradores_por_funcao("Coletor")
    return JsonResponse({"quantidade_coletores": quantidade_coletores})

@require_GET
def colaboradores_lista_inativos(request):
    colaboradores = Colaborador.objects.filter(status="INATIVO", tipo__in=TIPO_FUNCAO) \
        .values_list("nome", "tipo").distinct()

    nomes = [colab[0] for colab in colaboradores]
    tipos = list({colab[1] for colab in colaboradores})  

    return JsonResponse({
        "colaboradores_lista": nomes,
        "colaboradores_tipo": tipos,
    })