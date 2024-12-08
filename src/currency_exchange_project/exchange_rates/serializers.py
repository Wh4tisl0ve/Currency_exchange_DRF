from decimal import Decimal, InvalidOperation

from rest_framework import serializers

from currencies.serializers import CurrencySerializer
from currencies.models import Currency

from .models import ExchangeRate


class ExchangeRateSerializer(serializers.ModelSerializer):
    base_currency = CurrencySerializer(read_only=True)
    target_currency = CurrencySerializer(read_only=True)

    class Meta:
        model = ExchangeRate
        fields = [
            "id",
            "base_currency",
            "target_currency",
            "rate",
        ]
