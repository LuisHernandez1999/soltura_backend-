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

@csrf_exempt
@require_POST
def criar_veiculo(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)

    campos_obrigatorios = {'prefixo', 'tipo', 'placa_veiculo'}
    if not campos_obrigatorios.issubset(data):
        return JsonResponse({'erro': 'Campos obrigatórios ausentes.'}, status=400)

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
        custo_manutencao=custo_manutencao
    )

    return JsonResponse({'mensagem': 'Veículo criado com sucesso.', 'veiculo': model_to_dict(novo_veiculo)}, status=201)

@require_GET
def veiculos_lista_ativos(_request):
    cache_key = "veiculos_lista_ativos"
    placas_ativas = cache.get_or_set(
        cache_key,
        lambda: list(Veiculo.objects.filter(status='Ativo').values_list("placa_veiculo", flat=True)),
        timeout=3600  
    )
    return JsonResponse({"veiculos_lista_ativos": placas_ativas})

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
