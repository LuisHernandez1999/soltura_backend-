from ...models.models import Soltura
from django.utils.timezone import now



def tipos_veiculos_soltos_no_dia():
    try:
        hoje = now().date()
        quantidade_basculante = Soltura.objects.filter(
            tipo_veiculo='Basculante',
            data=hoje
        ).count()

        quantidade_bau = Soltura.objects.filter(
            tipo_veiculo='Baú',
            data=hoje
        ).count()

        quantidade_seletolix = Soltura.objects.filter(
            tipo_veiculo='Seletolix',
            data=hoje
        ).count()

        return {
            'Basculante': quantidade_basculante,
            'Baú': quantidade_bau,
            'Seletolix': quantidade_seletolix,
        }

    except Exception as e:
        raise Exception(f"Erro ao contar tipos de veículos soltos no dia: {str(e)}")



    
