from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Currency
from .validators import CurrencyCodeValidators


class CurrencySerializer(serializers.ModelSerializer):
    Code = serializers.CharField(
        min_length=3,
        max_length=3,
        validators=[CurrencyCodeValidators()],
    )
    FullName = serializers.CharField(max_length=20, required=False)
    Sign = serializers.CharField(max_length=3, required=False)

    class Meta:
        model = Currency
        fields = "__all__"


class CurrencyWriteSerializer(CurrencySerializer):
    FullName = serializers.CharField(max_length=20, required=True)
    Sign = serializers.CharField(max_length=3, required=True)
    Code = serializers.CharField(
        min_length=3,
        max_length=3,
        validators=[
            CurrencyCodeValidators(),
            UniqueValidator(
                queryset=Currency.objects.all(),
                message="Валюта с таким кодом уже существует",
            ),
        ],
    )

    def create(self, validated_data):
        validated_data["Code"] = validated_data["Code"].upper()

        return super().create(validated_data)
