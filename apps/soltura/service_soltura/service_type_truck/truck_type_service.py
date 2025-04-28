from ...models.models import Soltura
from django.utils.timezone import now

def tipos_veiculos_soltos_no_dia():
    try:
        hoje = now().date()
        
        # Obtenha as quantidades para cada tipo de veículo
        quantidade_basculante = Soltura.objects.filter(
            tipo_veiculo_selecionado='Basculante',
            data=hoje
        ).count()

        quantidade_bau = Soltura.objects.filter(
            tipo_veiculo_selecionado='Baú',
            data=hoje
        ).count()

        quantidade_seletolix = Soltura.objects.filter(
            tipo_veiculo_selecionado='Seletolix',
            data=hoje
        ).count()

        # Calcule o total de veículos soltos no dia
        total_veiculos = quantidade_basculante + quantidade_bau + quantidade_seletolix

        # Evite a divisão por zero caso o total seja 0
        if total_veiculos == 0:
            porcentagem_basculante = 0
            porcentagem_bau = 0
            porcentagem_seletolix = 0
        else:
            # Calcule as porcentagens
            porcentagem_basculante = (quantidade_basculante / total_veiculos) * 100
            porcentagem_bau = (quantidade_bau / total_veiculos) * 100
            porcentagem_seletolix = (quantidade_seletolix / total_veiculos) * 100

        # Retorne os dados com contagens e porcentagens
        return {
            'Basculante': {'contagem': quantidade_basculante, 'porcentagem': porcentagem_basculante},
            'Baú': {'contagem': quantidade_bau, 'porcentagem': porcentagem_bau},
            'Seletolix': {'contagem': quantidade_seletolix, 'porcentagem': porcentagem_seletolix},
        }

    except Exception as e:
        raise Exception(f"Erro ao contar tipos de veículos soltos no dia: {str(e)}")
