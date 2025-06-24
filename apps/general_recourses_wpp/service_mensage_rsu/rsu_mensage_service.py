from apps.soltura.models.models import Soltura 
from django.utils import timezone
from datetime import datetime
import pywhatkit

def mensage_rsu_wpp():
    data_hoje = timezone.localdate()
    recursos_gerais_seletiva_hoje = Soltura.objects.filter(tipo_servico='Rsu', data=data_hoje)

    pas = ['PA1', 'PA2', 'PA3', 'PA4']

    resultado_por_pa = {}

    for pa in pas:
        recurso_seletiva_pa = recursos_gerais_seletiva_hoje.filter(garagem=pa)

        total_coletores = recurso_seletiva_pa.values('coletores').count()
        total_veiculos = recurso_seletiva_pa.values('veiculo').count()

        resultado_por_pa[pa] = {
            'coletores': total_coletores,
            'veiculos': total_veiculos,
        }
    return resultado_por_pa


def enviar_mensagem_rsu_whatsapp():
    dados_pa_seletiva = mensage_rsu_wpp()

    numero_destino = "+55 62991104407"
    agora = datetime.now()
    horario_envio_str = agora.strftime("%H:%M")
    data_atual_str = agora.strftime("%d/%m/%Y")

    coletores_previstos = 45  # por PA
    veiculos_previstos = 15   # por PA

    def status_meta(previsto, atual):
        if atual >= previsto:
            return f"Meta atingida! ({atual}/{previsto})"
        else:
            falta = previsto - atual
            return f"Faltam {falta} para a meta ({atual}/{previsto})"

    mensagem = f"**Relatório de recursos em operação até o momento na RSU.**\n"
    mensagem += f"**Data:** {data_atual_str} | **Hora do envio:** {horario_envio_str}\n\n"

    for pa, dados in dados_pa_seletiva.items():
        mensagem += f"{pa}\n"
        mensagem += f"- **Coletores previstos:** {coletores_previstos}\n"
        mensagem += f"  • {status_meta(coletores_previstos, dados['coletores'])}\n"
        mensagem += f"- **Veículos previstos:** {veiculos_previstos}\n"
        mensagem += f"  • {status_meta(veiculos_previstos, dados['veiculos'])}\n\n"

    mensagem += "Atenciosamente,\nEquipe de Operações"

    pywhatkit.sendwhatmsg_instantly(numero_destino, mensagem, wait_time=20, tab_close=True)
    print(f"Mensagem resumo enviada para {numero_destino}")
