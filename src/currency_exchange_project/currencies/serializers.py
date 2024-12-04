from rest_framework import serializers
from .models import Currency


class CurrencySerializers(serializers.ModelSerializer):
    code = serializers.CharField(required=True, validators=[])
    full_name = serializers.CharField(required=False)
    sign = serializers.CharField(required=False)

    class Meta:
        model = Currency
        fields = ["id", "code", "full_name", "sign"]

    def validate_code(self, value: str):
        if not self.is_currency_code(value):
            raise serializers.ValidationError()

        return value

    def is_currency_code(self, value: str) -> bool:
        return len(value) == 3 and value.isalpha() and value.isascii()
