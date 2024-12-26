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

    def validate(self, attrs):
        if "rate" not in attrs:
            raise serializers.ValidationError("Отсутствует нужное поле формы")

        return attrs


class ExchangeRateWriteSerializer(ExchangeRateSerializer):
    baseCurrencyCode = serializers.CharField(
        min_length=3, max_length=3, source="base_currency", write_only=True
    )
    targetCurrencyCode = serializers.CharField(
        min_length=3, max_length=3, source="target_currency", write_only=True
    )

    class Meta:
        model = ExchangeRate
        fields = "__all__"

    def validate(self, attrs):
        base_currency = attrs.get("base_currency")
        target_currency = attrs.get("target_currency")

        if ExchangeRate.objects.filter(
            base_currency=base_currency, target_currency=target_currency
        ).exists():
            raise serializers.ValidationError(
                "Валютная пара с таким кодом уже существует"
            )

        return attrs

    def create(self, validated_data):
        exchange_rate = ExchangeRate(**validated_data)
        exchange_rate.save()

        return exchange_rate

    def validate_baseCurrencyCode(self, value):
        return get_object_or_404(Currency, Code=value.upper())

    def validate_targetCurrencyCode(self, value):
        return get_object_or_404(Currency, Code=value.upper())
