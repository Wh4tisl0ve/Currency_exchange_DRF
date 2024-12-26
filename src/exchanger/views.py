from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from currencies.models import Currency
from .service import ExchangerService
from exchanger.serializers import (
    ExchangerResponseSerializer,
    ExchangerRequestSerializer,
)


class ExchangerView(APIView):
    def get(self, request):
        serializer_request = ExchangerRequestSerializer(data=request.query_params)
        serializer_request.is_valid(raise_exception=True)

        base_currency = get_object_or_404(
            Currency, Code=request.query_params.get("base").upper()
        )
        target_currency = get_object_or_404(
            Currency, Code=request.query_params.get("target").upper()
        )

        rate_dto = ExchangerService.perform_currency_exchange(
            base_currency, target_currency, request.query_params.get("amount")
        )

        serializer_response = ExchangerResponseSerializer(rate_dto)

        return Response(serializer_response.data)
