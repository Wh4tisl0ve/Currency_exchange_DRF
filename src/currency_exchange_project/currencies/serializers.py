from rest_framework import serializers

from .models import Currency
from .validators import CurrencyCodeValidators


class CurrencySerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, validators=[CurrencyCodeValidators()])
    full_name = serializers.CharField(required=False)
    sign = serializers.CharField(required=False)

    class Meta:
        model = Currency
        fields = "__all__"


class CurrencyWriteSerializer(CurrencySerializer):
    full_name = serializers.CharField(required=True)
    sign = serializers.CharField(required=True)

    def validate_empty_values(self, data):
        if "code" not in data:
            raise serializers.ValidationError(
                {"detail": "Поле code обязательно для заполнения"}
            )

        if "full_name" not in data:
            raise serializers.ValidationError(
                {"detail": "Поле full_name обязательно для заполнения"}
            )

        if "sign" not in data:
            raise serializers.ValidationError(
                {"detail": "Поле sign обязательно для заполнения"}
            )

        return super().validate_empty_values(data)
