from typing import Dict

from django.conf import settings

from core.base_api import BaseRequestsAPI


async def create_loan_payback(data: Dict, type_loan: str = "loan") -> Dict:
    endpoint: str = ""

    if type_loan == "loan":
        endpoint = settings.API_PAWN_PAY_BACK

    else:
        # TODO: endpoint = settings.API_CREDIT_PAY_BACK
        raise Exception("Not fount endpoint from type credit")

    request = BaseRequestsAPI()

    return await request.arequest_post(endpoint, data)
