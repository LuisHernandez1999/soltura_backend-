from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.db.models import Exists, OuterRef
from django.core.cache import cache
from django.db.models import Q
import json
from .models import Veiculo, HistoricoManutencao, calcular_tempo_manutencao, VeiculoValidator
from django.db.models import Count

@csrf_exempt
@require_POST
def criar_veiculo(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)

    campos_obrigatorios = {'prefixo', 'tipo', 'placa_veiculo'}
    if not campos_obrigatorios.issubset(data):
       print(" Dados recebidos (parciais ou errados):", data)
       print(f"❗ Campos obrigatórios ausentes. Esperados: {campos_obrigatorios}")
       return JsonResponse({'erro': f'Campos obrigatórios ausentes. Esperados: {campos_obrigatorios}'}, status=400)

    try:
        VeiculoValidator.validar_placa(data['placa_veiculo'])
        VeiculoValidator.validar_tipo(data['tipo'])
    except ValidationError as e:
        return JsonResponse({'erro': str(e)}, status=400)
    if Veiculo.objects.filter(Q(prefixo=data['prefixo']) | Q(placa_veiculo=data['placa_veiculo'])).exists():
        return JsonResponse({'erro': 'Veículo já cadastrado.'}, status=409)
    dias_manutencao = calcular_tempo_manutencao(data.get('data_manutencao'), data.get('data_saida')) or 0
    custo_manutencao = float(data.get('custo_manutencao', 0)) * dias_manutencao if dias_manutencao > 0 else 0

    novo_veiculo = Veiculo.objects.create(
        prefixo=data['prefixo'],
        tipo=data['tipo'],
        placa_veiculo=data['placa_veiculo'],
        status=data.get('status'),
        motivo_inatividade=data.get('motivo_inatividade'),
        data_manutencao=data.get('data_manutencao'),
        data_saida=data.get('data_saida'),
        custo_manutencao=custo_manutencao,
        tipo_servico_usuario = data.get('tipo_servico_usuario')
    )

    return JsonResponse({'mensagem': 'Veículo criado com sucesso.', 'veiculo': model_to_dict(novo_veiculo)}, status=201)
@require_GET
def veiculos_lista_ativos(request):
    cache_key = "veiculos_lista_ativos"
    veiculos_ativos = cache.get_or_set(
        cache_key,
        lambda: list(Veiculo.objects.filter(status='Ativo').values("prefixo")),
        timeout=3600  
    )
    return JsonResponse({"veiculos_lista_ativos": veiculos_ativos})

@csrf_exempt
@require_POST
def editar_veiculo(request, veiculo_id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)

    campos_permitidos = {'prefixo', 'tipo', 'placa_veiculo', 'status', 'motivo_inatividade', 'data_manutencao', 'data_saida', 'custo_manutencao'}
    data = {key: data[key] for key in data if key in campos_permitidos}
    
    if 'placa_veiculo' in data:
        try:
            VeiculoValidator.validar_placa(data['placa_veiculo'])
        except ValidationError as e:
            return JsonResponse({'erro': str(e)}, status=400)
        if Veiculo.objects.filter(placa_veiculo=data['placa_veiculo']).exclude(id=veiculo_id).exists():
            return JsonResponse({'erro': 'Placa já cadastrada.'}, status=409)

    dias_manutencao = calcular_tempo_manutencao(data.get('data_manutencao'), data.get('data_saida')) or 0
    data['custo_manutencao'] = float(data.get('custo_manutencao', 0)) * dias_manutencao if dias_manutencao > 0 else 0
    
    Veiculo.objects.filter(id=veiculo_id).update(**data)
    veiculo_atualizado = Veiculo.objects.values().get(id=veiculo_id)
    return JsonResponse({'mensagem': 'Veículo atualizado.', 'veiculo': veiculo_atualizado}, status=200)

@require_GET
def historico_manutencao_veiculo(_, veiculo_id):
    historico = HistoricoManutencao.objects.filter(veiculo_id=veiculo_id).values(
        'data_manutencao', 'data_saida', 'custo_manutencao', 'descricao_manutencao'
    )
    return JsonResponse({'historico_manutencao': list(historico)}, json_dumps_params={'ensure_ascii': False})

def contagem_remocao_ativos(request):
    if request.method == 'GET':
        count_remocao_ativos = Veiculo.objects.filter(tipo_servico_veiculo='Remoção', status='Ativo').only('id').count()
        return JsonResponse({'count_remocao_ativos': count_remocao_ativos})
    return JsonResponse({'error': 'metodo nao permitido'}, status=405)

def contagem_remocao_inativos(request):
    if request.method == 'GET':
        count_remocao_inativos = Veiculo.objects.filter(tipo_servico_veiculo='Remoção', status='Inativo').only('id').count()

        return JsonResponse({'count_remocao_inativos': count_remocao_inativos})
    return JsonResponse({'error': 'metodo nao permitido'}, status=405)       


def contagem_total_remocao(request):
    if request.method == 'GET':
        count_remocao_ativos = Veiculo.objects.filter(tipo_servico_veiculo='Remoção', status='Ativo').only('id').count()
        count_remocao_inativos = Veiculo.objects.filter(tipo_servico_veiculo='Remoção', status='Inativo').only('id').count()
        total_remocao = count_remocao_ativos + count_remocao_inativos

        return JsonResponse({'total_remocao': total_remocao})
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)


########## seletiva

def contagem_seletiva_ativos(request):
    if request.method == 'GET':
        count_remocao_ativos = Veiculo.objects.filter(tipo_servico_veiculo='Seletiva', status='Ativo').only('id').count()
        return JsonResponse({'count_remocao_ativos': count_remocao_ativos})
    return JsonResponse({'error': 'metodo nao permitido'}, status=405)

def contagem_seletiva_inativos(request):
    if request.method == 'GET':
        count_remocao_inativos = Veiculo.objects.filter(tipo_servico_veiculo='Seletiva', status='Inativo').only('id').count()

        return JsonResponse({'count_remocao_inativos': count_remocao_inativos})
    return JsonResponse({'error': 'metodo nao permitido'}, status=405)       


def contagem_total_seletiva(request):
    if request.method == 'GET':
        count_remocao_ativos = Veiculo.objects.filter(tipo_servico_veiculo='Seletiva', status='Ativo').only('id').count()
        count_remocao_inativos = Veiculo.objects.filter(tipo_servico_veiculo='Seletiva', status='Inativo').only('id').count()
        total_remocao = count_remocao_ativos + count_remocao_inativos
        return JsonResponse({'total_remocao': total_remocao})
    return JsonResponse({'error': 'Método não permitido'}, status=405)