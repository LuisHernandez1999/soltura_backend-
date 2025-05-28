from apps.equipamentos.models import Equipamento

def listar_prefixos_e_implementos():
    equipamentos = Equipamento.objects.all()
    resultado = []
    for eqp in equipamentos:
        resultado.append({
            'prefixo': eqp.prefixo_equipamento,
            'implemento': eqp.implemento,
        })
    return resultado
