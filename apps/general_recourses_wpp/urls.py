from django.urls import path

from views_mensage_rsu.rsu_mensage_views import enviar_relatorio_whatsapp_view


urlpatterns=[
    path('general_recourses_wpp/enviar_xlsx/',enviar_relatorio_whatsapp_view,name='enviar_mensagem')
]