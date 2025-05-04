from django.urls import path
from averiguacao.views_averiguacao.averiguacao_create_views.create_views import criar_averiguacao
from averiguacao.views_averiguacao.update_averiguacao_views.update_averiguacao_views import update_averiguacao
from averiguacao.views_averiguacao.get_averiguacao_views.get_averiguacao_views import get_averiguacao
from averiguacao.views_averiguacao.delete_averiguacao_views.averiguacao_delete_views import delete_averiguacao
urlpatterns = [
    path('averiguacao/create/',criar_averiguacao, name='create_averiguacao'),
    path('averiguacao/update/', update_averiguacao, name='update_averiguacao'),
    path('averiguacao/get/', get_averiguacao, name='get_averiguacao'),
    path('averiguacao/delete/', delete_averiguacao, name='delete_averiguacao'),
]
