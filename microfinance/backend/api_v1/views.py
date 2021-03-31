import re
import json

from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.conf import settings

from rest_framework_jwt.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

import httpx

from core.base_api import BaseRequestsAPI, BaseViewFromAPI, BaseProxyApi
from core.soap import astart_transaction
from authentication.jwt_helpers import decode_token2dict
from .serializers import (
    RefreshEmailSerializer,
    RefreshPasswordSerializer,
    TokenSerializer,
    PawnTicketOperationsSerializer,
    PawnPropertiesSerializer,
    ProlongationPawnTicketSerializer,
    LoanPayBackSerializer,
    CheckStatusSerializer,
)
from services.prolongation import create_loan_prolongation
from services.pay_back import create_loan_payback
from core.soap import astatus_transaction


class ProfileInfoAPI(APIView, BaseProxyApi, BaseRequestsAPI):
    permission_classes = (AllowAny, )

    @method_decorator(async_to_sync)
    async def post(self, request):
        token = self.valid_request(request)
        
        if not token:
            return Response({"errors": [{"code": 4, "text": "Нет доступа"}]}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            resp = await self.arequest_post(settings.API_CLIENT_INFO, {"token": token})
        
        except httpx.ConnectTimeout:
            return Response({"errors": [{"code": 500, "text": "Непредвиденная ошибка"}]},
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            resp_data = resp.json()
            errors = self.get_errors(resp_data)
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(resp_data, status=status.HTTP_200_OK)

        except PermissionDenied:
            return Response({"errors": [{"code": 4, "text": "Срок действия сессии истек"}]},
                            status=status.HTTP_403_FORBIDDEN)
        
        except Exception:
            pass
        
        return Response({"errors": [{"code": 500, "text": "Непредвиденная ошибка"}]},
                        status=status.HTTP_400_BAD_REQUEST)
    
    
class RefreshEmailFromAPI(APIView, BaseProxyApi, BaseRequestsAPI):
    permission_classes = (AllowAny,)
    serializer_class = RefreshEmailSerializer

    @method_decorator(async_to_sync)
    async def post(self, request):
        token = self.valid_request(request)
    
        if not token:
            return Response({"errors": [{"code": 4, "text": "Нет доступа"}]}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
    
            try:
                resp = await self.arequest_post(settings.API_REFRESH_EMAIL, data)
        
            except (httpx.ConnectTimeout, httpx.ReadTimeout):
                return Response({"errors": [{"code": 500, "text": "Непредвиденная ошибка"}]},
                                status=status.HTTP_400_BAD_REQUEST)
        
            try:
                resp_data = resp.json()
                try:
                    errors = self.get_errors(resp_data)

                except PermissionDenied:
                    return Response({"errors": [{"code": 4, "text": "Срок действия сессии истек"}]},
                                    status=status.HTTP_403_FORBIDDEN)
                if errors:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(resp_data, status=status.HTTP_200_OK)
        
            except Exception:
                pass
    
        return Response({"error_fields": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RefreshPasswordFromAPI(APIView, BaseProxyApi, BaseRequestsAPI):
    permission_classes = (AllowAny,)
    serializer_class = RefreshPasswordSerializer
    
    @method_decorator(async_to_sync)
    async def post(self, request):
        token = self.valid_request(request)
        
        if not token:
            return Response({"errors": [{"code": 4, "text": "Нет доступа"}]}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            
            try:
                resp = await self.arequest_post(settings.API_REFRESH_PASSWORD, data)
            
            except (httpx.ConnectTimeout, httpx.ReadTimeout):
                return Response({"errors": [{"code": 500, "text": "Непредвиденная ошибка"}]},
                                status=status.HTTP_400_BAD_REQUEST)
            
            try:
                resp_data = resp.json()
                try:
                    errors = self.get_errors(resp_data)

                except PermissionDenied:
                    return Response({"errors": [{"code": 4, "text": "Срок действия сессии истек"}]},
                                    status=status.HTTP_403_FORBIDDEN)
                
                if errors:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(resp_data, status=status.HTTP_200_OK)
            
            except Exception:
                pass
        
        return Response({"error_fields": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

# TezLombard API
class PawnTicketListFromAPI(BaseViewFromAPI):
    serializer_class = TokenSerializer
    endpoint_api = settings.API_PAWN_TICKET_LIST

    def _response(self, resp: httpx.Response) -> Response:
        try:
            resp_data = resp.json()

            try:
                errors = self.get_errors(resp_data)

            except PermissionDenied:
                return Response({"errors": [{"code": 4, "text": "Срок действия сессии истек"}]},
                                status=status.HTTP_403_FORBIDDEN)

            if errors:
                return Response({"loanList": None}, status=status.HTTP_200_OK)

            return Response(resp_data["data"], status=status.HTTP_200_OK)

        except Exception as err:
            return Response({"loanList": None}, status=status.HTTP_200_OK)


class PawnTicketOperationsFromAPI(BaseViewFromAPI):
    serializer_class = PawnTicketOperationsSerializer
    endpoint_api = settings.API_PAWN_TICKET_OPERATIONS


class PawnTicketPropertyListAPI(BaseViewFromAPI):
    serializer_class = PawnTicketOperationsSerializer
    endpoint_api = settings.API_PAWN_PROPERTY_LIST


class PawnTicketPropertiesAPI(BaseViewFromAPI):
    serializer_class = PawnPropertiesSerializer
    endpoint_api = settings.API_PAWN_PROPERTIES


class PawnTicketDocumentsAPI(BaseViewFromAPI):
    serializer_class = PawnTicketOperationsSerializer
    endpoint_api = settings.API_PAWN_DOCUMENTS
    pattern_body = re.compile(r'<body>(.*?)</body>')

    def _response(self, resp: httpx.Response) -> HttpResponse:
        """
        @Override
        """
        body = self.pattern_body.findall(resp.text)
        if body:
            return HttpResponse(body[0])

        return HttpResponse("")


class PawnTicketCurrentOverdraftAPI(BaseViewFromAPI):
    serializer_class = PawnTicketOperationsSerializer
    endpoint_api = settings.API_PAWN_CURRENT_OVERDRAFT


# TezCredit API
class CreditListFromAPI(BaseViewFromAPI):
    serializer_class = TokenSerializer
    endpoint_api = settings.API_CREDIT_LIST

    def _response(self, resp: httpx.Response) -> Response:
        try:
            resp_data = resp.json()

            try:
                errors = self.get_errors(resp_data)

            except PermissionDenied:
                return Response({"errors": [{"code": 4, "text": "Срок действия сессии истек"}]},
                                status=status.HTTP_403_FORBIDDEN)

            if errors:
                return Response({"loanList": None}, status=status.HTTP_200_OK)

            return Response(resp_data["data"], status=status.HTTP_200_OK)

        except Exception as err:
            return Response({"loanList": None}, status=status.HTTP_200_OK)


class CreditOperationsFromAPI(BaseViewFromAPI):
    serializer_class = PawnTicketOperationsSerializer
    endpoint_api = settings.API_CREDIT_OPERATIONS


class CreditPropertyListAPI(BaseViewFromAPI):
    serializer_class = PawnTicketOperationsSerializer
    endpoint_api = settings.API_CREDIT_PROPERTY_LIST


class CreditPropertiesAPI(BaseViewFromAPI):
    serializer_class = PawnPropertiesSerializer
    endpoint_api = settings.API_CREDIT_PROPERTIES


class CreditDocumentsAPI(BaseViewFromAPI):
    serializer_class = PawnTicketOperationsSerializer
    endpoint_api = settings.API_CREDIT_DOCUMENTS
    pattern_body = re.compile(r'<body>(.*?)</body>')

    def _response(self, resp: httpx.Response) -> HttpResponse:
        """
        @Override
        """
        body = self.pattern_body.findall(resp.text)
        if body:
            return HttpResponse(body[0])

        return HttpResponse("")


class CreditCurrentOverdraftAPI(BaseViewFromAPI):
    serializer_class = PawnTicketOperationsSerializer
    endpoint_api = settings.API_CREDIT_CURRENT_OVERDRAFT


class ProlongationPawnTicketAPIView(APIView):
    serializer_class = ProlongationPawnTicketSerializer
    permission_classes = (AllowAny,)

    @method_decorator(async_to_sync)
    async def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return_url = settings.PROCESSING_RETURN_URL.format("loan", serializer.data['prd'],
                                                           serializer.data['referenceId'], "pro")
        # print("Prolongation return_url: ", return_url)
        soap_data = {
            "returnURL": return_url,
            "customerReference": serializer.data['referenceId'],
            "orderId": serializer.validated_data['loanId'],
            "amount": serializer.validated_data['totalSum'],
        }

        resp = await astart_transaction(soap_data, "loan")
        # print("Prolongation astart_transaction: ", resp)
        return Response({
            "customerReference": resp.customerReference,
            "errorDescription": resp.errorDescription,
            "redirectURL": resp.redirectURL,
            "success": resp.success,
        }, status=status.HTTP_200_OK)


class LoanPayBackAPIView(APIView):
    serializer_class = LoanPayBackSerializer
    permission_classes = (AllowAny,)

    @method_decorator(async_to_sync)
    async def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return_url = settings.PROCESSING_RETURN_URL.format("loan", serializer.data['prd'],
                                                           serializer.data['referenceId'], "rep")
        # print("Rep return_url: ", return_url)
        soap_data = {
            "returnURL": return_url,
            "customerReference": serializer.data['referenceId'],
            "orderId": serializer.validated_data['loanId'],
            "amount": serializer.validated_data['mainDebtSum'],
        }

        resp = await astart_transaction(soap_data, "loan")
        # print("Rep astart_transaction: ", resp)
        return Response({
            "customerReference": resp.customerReference,
            "errorDescription": resp.errorDescription,
            "redirectURL": resp.redirectURL,
            "success": resp.success,
        }, status=status.HTTP_200_OK)


class CheckStatusAPIView(APIView):
    serializer_class = CheckStatusSerializer
    permission_classes = (AllowAny,)

    @method_decorator(async_to_sync)
    async def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            return_processing_data = decode_token2dict(serializer.validated_data["token_processing"])

        except Exception as err:
            return Response({"error": "error decode processingData", "status": None},
                            status=status.HTTP_400_BAD_REQUEST)

        status_transaction = \
            await astatus_transaction(serializer.validated_data["reference_id"],
                                            serializer.validated_data["type_loan"])
        # print("status_transaction: ", status_transaction)
        if status_transaction.transactionStatus == "PAID":
            _status_transaction = {
                "transactionStatus": status_transaction.transactionStatus,
                "amountAuthorised": status_transaction.amountAuthorised,
                "amountRequested": status_transaction.amountRequested,
                "amountSettled": status_transaction.amountSettled,
                "bankRRN": status_transaction.bankRRN,
                "merchantLocalDateTime": status_transaction.merchantLocalDateTime,
                "orderId": status_transaction.orderId,
                "purchaserName": status_transaction.purchaserName,
            }
            if serializer.validated_data["type_transaction"] == "pro":
                # prolongation
                resp_api = await create_loan_prolongation({
                    "token": serializer.validated_data["token"],
                    "loanId": return_processing_data["loanId"],
                    "newPeriod": return_processing_data["newPeriod"],
                    "mainDebtSum": return_processing_data["mainDebtSum"],
                    "referenceId": serializer.validated_data["reference_id"],
                }, serializer.validated_data["type_loan"])

                try:
                    # print("pro create_loan_prolongation: ", resp_api.json())
                    resp_data = resp_api.json()["data"]
                    resp_data["_type"] = "collateralized" if serializer.validated_data["type_loan"] == "loan" \
                        else "unsecured"
                    resp_data["typeTransaction"] = "prolongation"
                    resp_data["status"] = _status_transaction
                    return Response(resp_data, status=status.HTTP_200_OK)

                except Exception as err:
                    return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

            elif serializer.validated_data["type_transaction"] == "rep":
                # repayment
                resp_api = await create_loan_payback({
                    "token": serializer.validated_data["token"],
                    "loanId": return_processing_data["loanId"],
                    "mainDebtSum": return_processing_data["mainDebtSum"],
                    "referenceId": serializer.validated_data["reference_id"],
                }, serializer.validated_data["type_loan"])
                try:
                    # print("rep create_loan_payback: ", resp_api.json())
                    resp_data = resp_api.json()["data"]
                    resp_data["_type"] = "collateralized" if serializer.validated_data["type_loan"] == "loan" \
                        else "unsecured"
                    resp_data["typeTransaction"] = "repayment"
                    resp_data["status"] = _status_transaction
                    return Response(resp_data, status=status.HTTP_200_OK)

                except Exception as err:
                    return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "not transaction", "status": status_transaction.transactionStatus},
                        status=status.HTTP_400_BAD_REQUEST)


async def is_live(requests) -> HttpResponse:
    return HttpResponse(json.dumps({"response": True}), content_type="application/json", status=200)

