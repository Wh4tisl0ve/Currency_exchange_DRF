from rest_framework import serializers

from currencies.serializers import CurrencySerializer


class ExchangerSerializer(serializers.Serializer):
    base_currency = CurrencySerializer(read_only=True)
    target_currency = CurrencySerializer(read_only=True)
    rate = serializers.DecimalField(max_digits=10, decimal_places=4)
    amount = serializers.DecimalField(max_digits=10, decimal_places=4)
    convertedAmount = serializers.DecimalField(max_digits=10, decimal_places=4)
