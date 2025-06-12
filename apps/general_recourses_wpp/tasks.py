from celery import shared_task



@shared_task
def enviar_mensagem_rsu_whatsapp_task():
    from .service_mensage_rsu.rsu_mensage_service import enviar_mensagem_rsu_whatsapp 
    enviar_mensagem_rsu_whatsapp()



@shared_task
def enviar_mensagem_seletiva_whatsapp_task():
    from .service_mensage_seletiva.seletiva_mensage_service import mensagem_wpp_seletiva
    mensagem_wpp_seletiva()