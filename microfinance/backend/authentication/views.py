from datetime import datetime, timedelta
from typing import Union

from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from asgiref.sync import async_to_sync
from django.conf import settings

from rest_framework_jwt.views import APIView, JSONWebTokenAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.compat import get_username_field
from rest_framework import status

import httpx

from core.cors import CorsAllow
from authentication.jwt_helpers import create_token_from_dict
from core.base_api import BaseRequestsAPI
from .serializers import LoginSerializer, PhoneSerializer, LoginFromCodeSerializer, UserSerializer, \
    LoginSerializerFromAPI, PhoneSerializerAPI, PhoneSerializerConfirmAPI, RecoveryPasswordSerializer
from .models import User


# Максимальное количество неудачных попыток войти в свой профиль
COUNT_FAILED_ATTEMPT = getattr(settings, "COUNT_FAILED_ATTEMPT", 2)
# Время бана пользователя при исчерпании всех доступных попыток
BAN_TIME = getattr(settings, "BAN_TIME", timedelta(minutes=30))


class AuthJSONWebToken(JSONWebTokenAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # проверяем есть ли на самом деле такой юзер
        data = {
            self.username_field: request.data.get(self.username_field),
        }
        try:
            _user = User.objects.get(**data)
    
        except User.DoesNotExist:
            return Response({"error": "not valid data"}, status=status.HTTP_400_BAD_REQUEST)

        # проверяем какая попытка аутентифицироваться
        if _user.profile.failed_attempt >= COUNT_FAILED_ATTEMPT:
            if _user.profile.updated_at.replace(tzinfo=None) + BAN_TIME > datetime.today():
                # пользователь превысил количество провальных попыток аутентификации и забанен на BAN_TIME
                # time_delta = (_user.profile.updated_at.replace(tzinfo=None) + BAN_TIME) - datetime.today()
                return Response({"error": "User account is banned", "time": BAN_TIME},
                                status=status.HTTP_400_BAD_REQUEST)
            
            else:
                _user.profile.failed_attempt = 0
                _user.profile.save()
            
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            
            # залогируем пользователя в сессии
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # логируем количество неудачных попыток
        _user.profile.failed_attempt += 1
        _user.profile.save()
        return Response({"error": "not valid data", "attempt": _user.profile.failed_attempt},
                        status=status.HTTP_400_BAD_REQUEST)
    
    @property
    def username_field(self):
        return get_username_field()
        
    
class LogoutApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        logout(request)
        return Response({"response": True}, status=status.HTTP_200_OK)

    def get(self, request):
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    
class GetCodeFromPhoneApiView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PhoneSerializer
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            self.send_sms(serializer.data["phone"], serializer.data["code"])
        
        return Response({"response": True}, status=status.HTTP_200_OK)

    def get(self, request):
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    def send_sms(self, phone: str, code: str):
        print(f"{phone}: {code}")


class AuthFromSMSApiView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginFromCodeSerializer
    
    def post(self, request):
        data = request.data
        
        if data.get("code") is None:
            Response({}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        login(request, serializer.data["user"])
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    
class RestorePasswordApiView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    
    def update(self, request):
        data = request.data
        
        if data.get("code") is None:
            Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get(self, request):
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class AuthJSONWebTokenFromAPI(APIView, BaseRequestsAPI):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializerFromAPI

    # @method_decorator(CorsAllow())
    @method_decorator(async_to_sync)
    async def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():

            try:
                resp = await self.arequest_post(settings.API_AUTH_PSWD, data)
            
            except (httpx.ConnectTimeout, httpx.ReadTimeout):
                return Response({"errors": [{"code": "api", "text": "Непредвиденная ошибка"}]},
                                status=status.HTTP_400_BAD_REQUEST)
            
            if resp.is_error:
                return Response({"errors": [{"code": "api", "text": "Непредвиденная ошибка"}]},
                                status=status.HTTP_400_BAD_REQUEST)
            
            try:
                resp_data = resp.json()
                if resp_data.get("errors"):
                    return Response(resp_data, status=status.HTTP_400_BAD_REQUEST)
                
                serializer.validated_data["token"] = resp_data["data"]["token"]
                
                if serializer.data.get("app_name"):
                    return Response({"response": True, "token_app": serializer.data["token_app"]},
                                    status=status.HTTP_200_OK)

                return Response(serializer.data, status=status.HTTP_200_OK)
            
            except Exception:
                return Response({"errors": [{"code": "api", "text": "Непредвиденная ошибка"}]},
                                status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthSendSMSProxyFromAPI(APIView, BaseRequestsAPI):
    permission_classes = (AllowAny,)
    serializer_class = PhoneSerializerAPI

    @method_decorator(CorsAllow())
    @method_decorator(async_to_sync)
    async def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            try:
                resp = await self.arequest_post(settings.API_AUTH_SEND_SMS, data)
            
            except (httpx.ConnectTimeout, httpx.ReadTimeout):
                return Response({"errors": [{"code": "api", "text": "Непредвиденная ошибка"}]},
                                 status=status.HTTP_400_BAD_REQUEST)
            
            try:
                resp_data = resp.json()
                errors = self.get_errors(resp_data)
                if errors:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({"sent": True}, status=status.HTTP_200_OK)
            
            except Exception:
                return Response({"errors": [{"code": "api", "text": "Непредвиденная ошибка"}]},
                                status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthSMSConfirmFromAPI(APIView, BaseRequestsAPI):
    permission_classes = (AllowAny,)
    serializer_class = PhoneSerializerConfirmAPI

    @method_decorator(CorsAllow())
    @method_decorator(async_to_sync)
    async def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            try:
                resp = await self.arequest_post(settings.API_AUTH_CONFIRM_SMS, data)
            
            except (httpx.ConnectTimeout, httpx.ReadTimeout):
                return Response({"errors": [{"code": "api", "text": "Непредвиденная ошибка"}]},
                                status=status.HTTP_400_BAD_REQUEST)
            
            try:
                resp_data = resp.json()
                errors = self.get_errors(resp_data)
                if errors:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

                serializer.validated_data["token"] = resp_data["data"]["token"]
                
                # if data.get("app_name") and resp_data["data"].get("token"):
                #     token_app = create_token_from_dict({
                #         "token": resp_data["data"]["token"],
                #         "app": data["app_name"],
                #     }, 60)
                #
                #     return Response({"response": True, "token_app": token_app}, status=status.HTTP_200_OK)
                # return Response(resp_data["data"], status=status.HTTP_200_OK)

                if serializer.data.get("app_name"):
                    return Response({"response": True, "token_app": serializer.data["token_app"]},
                                    status=status.HTTP_200_OK)

                return Response(serializer.data, status=status.HTTP_200_OK)
            
            except Exception:
                return Response({"errors": [{"code": "api", "text": "Непредвиденная ошибка"}]},
                                status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class RecoveryPasswordFromAPI(APIView, BaseRequestsAPI):
    permission_classes = (AllowAny,)
    serializer_class = RecoveryPasswordSerializer
    endpoint_api = settings.API_RECOVERY_PSWD

    @method_decorator(CorsAllow())
    @method_decorator(async_to_sync)
    async def post(self, request):
    
        if not self.serializer_class:
            raise Exception("Serializer class not initialized")
    
        data = request.data
        serializer = self.serializer_class(data=data)
    
        if serializer.is_valid():
            try:
                resp = await self.arequest_post(self.endpoint_api, data)
        
            except (httpx.ConnectTimeout, httpx.ReadTimeout):
                return Response({"errors": [{"code": "api", "text": "Непредвиденная ошибка"}]},
                                status=status.HTTP_400_BAD_REQUEST)
        
            try:
                resp_data = resp.json()
                errors = self.get_errors(resp_data)
                if errors:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
                return Response(resp_data["data"], status=status.HTTP_200_OK)
        
            except Exception:
                return Response({"errors": [{"code": "api", "text": "Непредвиденная ошибка"}]},
                                status=status.HTTP_400_BAD_REQUEST)
    
        return Response({"error_fields": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_errors(self, response) -> Union[dict, None]:
        if response.get("errors") and len(response["errors"]) > 0:
            _error = []
            for _err in response["errors"]:
                if _err["code"] in settings.PUBLIC_ERROR_CODE:
                    _error.append(_err)
                    
                elif _err["code"] == 16 or _err["code"] == 7:
                    return {"errors": [{'code': 16, 'text': 'Введены неверные данные'}]}
                
            if len(_error) > 0:
                return {"errors": _error}
    
        return None
