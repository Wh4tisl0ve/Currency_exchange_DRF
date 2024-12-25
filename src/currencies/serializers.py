from rest_framework import serializers

from .models import Currency
from .validators import CurrencyCodeValidators


class CurrencySerializer(serializers.ModelSerializer):
    Code = serializers.CharField(validators=[CurrencyCodeValidators()])
    FullName = serializers.CharField(required=False)
    Sign = serializers.CharField(required=False)

    class Meta:
        model = Currency
        fields = "__all__"


class CurrencyWriteSerializer(CurrencySerializer):
    FullName = serializers.CharField(required=True)
    Sign = serializers.CharField(required=True)

    def create(self, validated_data):
        validated_data["Code"] = validated_data["Code"].upper()

        return super().create(validated_data)
