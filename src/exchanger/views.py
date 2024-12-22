from rest_framework.views import APIView
from rest_framework.response import Response

from currencies.models import Currency
from .service import ExchangerService
from exchanger.serializers import ExchangerSerializer


class ExchangerView(APIView):
    exchange_service = ExchangerService
    serializer_class = ExchangerSerializer

    def get(self, request):
        base_currency = Currency.objects.get(Code=request.GET.get("from").upper())
        target_currency = Currency.objects.get(Code=request.GET.get("to").upper())

        service = self.exchange_service()
        rate_dto = service.perform_currency_exchange(
            base_currency, target_currency, request.GET.get("amount")
        )

        serializer = self.serializer_class(rate_dto)

        return Response(serializer.data)
