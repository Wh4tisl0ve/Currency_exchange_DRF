from decimal import Decimal, InvalidOperation

from django.shortcuts import get_object_or_404

from rest_framework import serializers

from currencies.serializers import CurrencySerializer
from currencies.models import Currency

from .models import ExchangeRate


class ExchangeRateSerializer(serializers.ModelSerializer):
    base_currency = CurrencySerializer(read_only=True)
    target_currency = CurrencySerializer(read_only=True)

    class Meta:
        model = ExchangeRate
        fields = "__all__"


class ExchangeRateWriteSerializer(ExchangeRateSerializer):
    baseCurrencyCode = serializers.CharField(source="base_currency", write_only=True)
    targetCurrencyCode = serializers.CharField(
        source="target_currency", write_only=True
    )

    class Meta:
        model = ExchangeRate
        fields = [
            "id",
            "baseCurrencyCode",
            "targetCurrencyCode",
            "base_currency",
            "target_currency",
            "rate",
        ]

    def create(self, validated_data):
        base_currency = validated_data.get("base_currency")
        target_currency = validated_data.get("target_currency")
        rate = validated_data.get("rate")

        exchange_rate = ExchangeRate(
            base_currency=base_currency,
            target_currency=target_currency,
            rate=rate,
        )
        exchange_rate.save()

        return exchange_rate

    def validate_baseCurrencyCode(self, value):
        return get_object_or_404(Currency, code=value.upper())

    def validate_targetCurrencyCode(self, value):
        return get_object_or_404(Currency, code=value.upper())

    def validate_empty_values(self, data):
        required_fields = ["baseCurrencyCode", "targetCurrencyCode", "rate"]

        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(
                    {"detail": f"Поле {field} обязательно для заполнения"}
                )

        return super().validate_empty_values(data)
