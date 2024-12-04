from rest_framework import serializers

from .models import ExchangeRate


class ExchangeRatesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = ["id", "base_currency", "target_currency", "rate"]