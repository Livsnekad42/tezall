from typing import Dict, Union
import json

from django.views.generic import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from asgiref.sync import async_to_sync

from authentication.jwt_helpers import decode_token2dict
from core.soap import astatus_transaction
from services.prolongation import create_loan_prolongation


APPS_REDIRECT: Dict[str, str] = {
    "aqsha": "https://tezaqsha.kz",
    "tez": "https://tezlombard.kz",
}


class IndexView(View):
    template_name = 'index.html'

    @method_decorator(async_to_sync)
    async def get(self, request, *args, **kwargs):
        
        user_data: Union[Dict, None] = None
        payment_data: Union[Dict, None] = None
        
        if request.GET.get("tokenApp"):
            try:
                data = decode_token2dict(request.GET["tokenApp"])
                if data and data.get("token"):
                    user_data = {}
                    user_data["token"] = data["token"]
                    user_data["phone"] = data.get("phone")
                    if data.get("app"):
                        user_data["redirect_url"] = APPS_REDIRECT.get(data["app"])
                    
                else:
                    user_data = None
                
            except Exception as e:
                user_data = None

        if request.GET.get("tl") and request.GET.get("prd") and request.GET.get("ref"):
            # пользователь вернулся от процессинга
            # пробрасываем гет параметры на сторону клиента
            payment_data = {
                "tl": request.GET["tl"],
                "prd": request.GET["prd"],
                "ref": request.GET["ref"],
                "tt": request.GET.get("tt")
            }

        return render(request, self.template_name, {
            'user_data': json.dumps(user_data) if user_data else None,
            'payment_data': json.dumps(payment_data) if payment_data else None,
        })

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
