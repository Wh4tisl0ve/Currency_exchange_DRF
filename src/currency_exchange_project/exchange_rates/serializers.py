from decimal import Decimal, InvalidOperation

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from currencies.serializers import CurrencySerializer
from currencies.models import Currency

from .models import ExchangeRate


class ExchangeRateSerializer(serializers.ModelSerializer):
    baseCurrencyCode = serializers.CharField(source="base_currency", write_only=True)
    targetCurrencyCode = serializers.CharField(
        source="target_currency", write_only=True
    )

    base_currency = CurrencySerializer(read_only=True)
    target_currency = CurrencySerializer(read_only=True)

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
        try:
            return Currency.objects.get(code=value.upper())
        except Currency.DoesNotExist:
            raise NotFound(f"Валюта с названием {value} не существует")

    def validate_targetCurrencyCode(self, value):
        try:
            return Currency.objects.get(code=value.upper())
        except Currency.DoesNotExist:
            raise NotFound(f"Валюта с названием {value} не существует")

    def validate_rate(self, value):
        try:
            return Decimal(str(value).replace(",", "."))
        except InvalidOperation:
            raise serializers.ValidationError("Поле rate содержит неверный формат")

    def validate_empty_values(self, data):
        if "baseCurrencyCode" not in data:
            raise serializers.ValidationError(
                {"detail": "Поле baseCurrencyCode обязательно для заполнения"}
            )

        if "targetCurrencyCode" not in data:
            raise serializers.ValidationError(
                {"detail": "Поле targetCurrencyCode обязательно для заполнения"}
            )

        if "rate" not in data:
            raise serializers.ValidationError(
                {"detail": "Поле rate обязательно для заполнения"}
            )

        return super().validate_empty_values(data)
