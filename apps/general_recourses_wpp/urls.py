from django.urls import path

from views_mensage_rsu.rsu_mensage_views import enviar_relatorio_whatsapp_view
from views_mensage_seletiva.seletiva_mensage_views import enviar_relatorio_seletiva_whatsapp_view

urlpatterns=[
    path('general_recourses_wpp/enviar_rsu_wpp/',enviar_relatorio_whatsapp_view,name='enviar_mensagem'),
    path('general_recourses_wpp/enviar_seletiva_wpp/',enviar_relatorio_seletiva_whatsapp_view,name='enviar_mensagem')
]