from typing import Dict

from django.conf import settings

from core.base_api import BaseRequestsAPI


async def create_loan_prolongation(data: Dict, type_loan: str = "loan") -> Dict:
    endpoint: str = ""

    if type_loan == "loan":
        endpoint = settings.API_PAWN_PROLONGATION

    else:
        # TODO: endpoint = settings.PAYMENT_PROCESSING_CREDIT
        raise Exception("Not fount endpoint from type credit")

    request = BaseRequestsAPI()

    return await request.arequest_post(endpoint, data)
