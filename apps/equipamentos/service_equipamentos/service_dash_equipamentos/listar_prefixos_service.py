from apps.equipamentos.models import Equipamento

def listar_prefixos_e_implementos():
    equipamentos = Equipamento.objects.all()

    resultado = []
    ativos = []
    inativos = []
    manutencao_count = 0
    garagem_count = 0  # Inicialização da variável

    for eqp in equipamentos:
        dados = {
            'prefixo': eqp.prefixo_equipamento,
            'status': eqp.status_equipamento,
            'motivo_inatividade':eqp.motivo_inatividade,
            'implemento': eqp.implemento
        }

        if eqp.status_equipamento == 'Inativo':
            motivo = eqp.motivo_inatividade
            dados['motivo_inatividade'] = motivo

            if motivo == 'Manutenção':
                manutencao_count += 1
            elif motivo == 'Em garagem':
                garagem_count += 1

            inativos.append(dados)

        elif eqp.status_equipamento == 'Ativo':
            ativos.append(dados)

        resultado.append(dados)

    return {
        'todos': resultado,
        'ativos': ativos,
        'inativos': inativos,
        'total': resultado,
        'contagem_total': len(resultado),
        'contagem_ativos': len(ativos),
        'contagem_inativos': len(inativos),
        'contagem_em_garagem': garagem_count,
        'contagem_manutencao': manutencao_count,
    }
