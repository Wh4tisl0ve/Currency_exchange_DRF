from rest_framework import serializers

from .models import Currency
from .validators import CurrencyCodeValidators


class CurrencySerializer(serializers.ModelSerializer):
    code = serializers.CharField(min_length=3, max_length=3, validators=[CurrencyCodeValidators()])
    fullname = serializers.CharField(max_length=20, required=False)
    sign = serializers.CharField(max_length=3, required=False)

    class Meta:
        model = Currency
        fields = "__all__"


class CurrencyWriteSerializer(CurrencySerializer):
    fullname = serializers.CharField(max_length=20, required=True)
    sign = serializers.CharField(max_length=3, required=True)

    def create(self, validated_data):
        validated_data["code"] = validated_data["code"].upper()

        return super().create(validated_data)
