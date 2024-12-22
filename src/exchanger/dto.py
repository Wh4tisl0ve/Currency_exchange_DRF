from dataclasses import dataclass
from decimal import Decimal

from currencies.models import Currency


@dataclass(frozen=True)
class ExchangerResponse:
    base_currency: Currency
    target_currency: Currency
    rate: Decimal
    amount: Decimal
    convertedAmount: Decimal
