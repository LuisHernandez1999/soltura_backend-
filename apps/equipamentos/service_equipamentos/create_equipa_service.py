from apps.equipamentos.models import Equipamento


def criar_equipamento(prefixo, implemento, status,motivo_inatividade):
    try:
        equipamento = Equipamento.objects.create(
            prefixo_equipamento=prefixo,
            implemento=implemento,
            status_equipamento=status,
            motivo_inatividade=motivo_inatividade,
        )
        print(f"equipamento criado com sucesso: {equipamento}")
        return equipamento
    except Exception as e:
        print(f"erro ao criar equipamento: {e}")
        return None
    