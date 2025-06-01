from apps.equipamentos.models import Equipamento

def listar_prefixos_e_implementos():
    equipamentos = Equipamento.objects.all()

    resultado = []
    ativos = []
    inativos = []
    manutencao_count = 0

    for eqp in equipamentos:
        dados = {
            'prefixo': eqp.prefixo_equipamento,
            'status': eqp.status_equipamento,
            'implemento':eqp.implemento
        }

        if eqp.status_equipamento == 'Inativo':
            dados['motivo_inatividade'] = eqp.motivo_inatividade  
            if eqp.motivo_inatividade == 'Em Manutenção':
                manutencao_count += 1

        resultado.append(dados)

        if eqp.status_equipamento == 'Ativo':
            ativos.append(dados)
        elif eqp.status_equipamento == 'Inativo':
            inativos.append(dados)

    total = resultado  

    return {
        'todos': resultado,
        'ativos': ativos,
        'inativos': inativos,
        'total': total,
        'contagem_total':len(total),
        'contagem_ativos': len(ativos),
        'contagem_inativos': len(inativos),
        'contagem_manutencao': manutencao_count,
    }
