from django.urls import path

from .views import AuthJSONWebTokenFromAPI, AuthSendSMSProxyFromAPI, AuthSMSConfirmFromAPI, \
    RecoveryPasswordFromAPI


urlpatterns = [
    path('loginApi/', AuthJSONWebTokenFromAPI.as_view(), name="loginApi"),
    path('sendSmsApi/', AuthSendSMSProxyFromAPI.as_view(), name="sendSmsApi"),
    path('confirmApi/', AuthSMSConfirmFromAPI.as_view(), name="confirmApi"),
    path('recovery/', RecoveryPasswordFromAPI.as_view(), name='recovery'),
]