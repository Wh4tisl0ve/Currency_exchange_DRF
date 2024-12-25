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
    exchanger_service = ExchangerService
    serializer_response_class = ExchangerResponseSerializer
    serializer_request_class = ExchangerRequestSerializer

    def get(self, request):
        serializer_request = self.serializer_request_class(data=request.GET)
        serializer_request.is_valid(raise_exception=True)

        base_currency = get_object_or_404(
            Currency, Code=request.GET.get("base").upper()
        )
        target_currency = get_object_or_404(
            Currency, Code=request.GET.get("target").upper()
        )

        rate_dto = self.exchanger_service().perform_currency_exchange(
            base_currency, target_currency, request.GET.get("amount")
        )

        serializer_response = self.serializer_response_class(rate_dto)

        return Response(serializer_response.data)
