from decimal import Decimal

from django.shortcuts import get_object_or_404

from currencies.models import Currency
from exchange_rates.models import ExchangeRate
from .dto import ExchangerResponse


class ExchangerService:
    def perform_currency_exchange(
        self, base_currency: Currency, target_currency: Currency, amount: float
    ) -> ExchangerResponse:
        try:
            return self.__calc_by_direct_rate(base_currency, target_currency, amount)
        except ExchangeRate.DoesNotExist:
            try:
                return self.__calc_by_reverse_rate(
                    base_currency, target_currency, amount
                )
            except ExchangeRate.DoesNotExist:
                return self.__calc_by_cross_rate(base_currency, target_currency, amount)

    def __calc_by_direct_rate(
        self, base_currency: Currency, target_currency: Currency, amount: float
    ) -> ExchangerResponse:
        direct_rate = ExchangeRate.objects.get(
            base_currency=base_currency, target_currency=target_currency
        )

        converted_amount = direct_rate.rate * Decimal(amount)

        return ExchangerResponse(
            base_currency, target_currency, direct_rate.rate, amount, converted_amount
        )

    def __calc_by_reverse_rate(
        self, base_currency: Currency, target_currency: Currency, amount: float
    ) -> ExchangerResponse:
        rate = ExchangeRate.objects.get(
            base_currency=target_currency, target_currency=base_currency
        )

        reverse_rate = Decimal(1) / rate.rate
        print(reverse_rate)
        converted_amount = reverse_rate * Decimal(amount)

        return ExchangerResponse(
            base_currency, target_currency, reverse_rate, amount, converted_amount
        )

    def __calc_by_cross_rate(
        self, base_currency: Currency, target_currency: Currency, amount: float
    ) -> ExchangerResponse:
        currency_usd = get_object_or_404(Currency, Code="USD")
        usd_base_exchange_rate = get_object_or_404(
            ExchangeRate, base_currency=currency_usd, target_currency=base_currency
        )

        usd_target_exchange_rate = get_object_or_404(
            ExchangeRate, base_currency=currency_usd, target_currency=target_currency
        )

        base_to_usd = (1 / usd_base_exchange_rate.rate) * Decimal(amount)
        converted_amount = base_to_usd * usd_target_exchange_rate.rate
        rate = converted_amount / Decimal(amount)

        return ExchangerResponse(
            base_currency, target_currency, rate, amount, converted_amount
        )
