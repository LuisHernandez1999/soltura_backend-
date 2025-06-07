from django.urls import path
from .service_captcha.captcha_service import get_captcha,verify_captcha


urlpatterns = [
    path('captcha/pegar/',get_captcha, name='get_captcha'),
    path('captcha/verificar',verify_captcha,name='captcha_verify')

]
