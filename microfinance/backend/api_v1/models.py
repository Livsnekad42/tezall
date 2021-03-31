from typing import Dict
from dataclasses import dataclass

from django.db import models


@dataclass
class ProlongationData:
    mainDebtSum: int
    newPeriod: int
    loanId: str


@dataclass
class RepaymentData:
    mainDebtSum: int
    loanId: str
