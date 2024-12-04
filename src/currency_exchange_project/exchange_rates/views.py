from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from currencies.models import Currency
from .models import ExchangeRate
from .serializer import ExchangeRatesSerializers


class ExchangeRatesList(APIView):
    serializer_class = ExchangeRatesSerializers

    def get(self, request):
        exchange_rates = ExchangeRate.objects.all()
        serializer = self.serializer_class(exchange_rates, many=True)
        return Response(serializer.data)

    def post(self, request):
        base_currency_request = Currency.objects.get(
            code=request.data.get("baseCurrencyCode")
        )
        target_currency_request = Currency.objects.get(
            code=request.data.get("targetCurrencyCode")
        )
        rate_request = request.data.get("rate")

        exchange_rate = ExchangeRate(
            base_currency=base_currency_request,
            target_currency=target_currency_request,
            rate=rate_request,
        )

        serializer = self.serializer_class(data=exchange_rate)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExchangeRatePairList(APIView):
    serializer_class = ExchangeRatesSerializers

    def get(self, request, currency_pair):

        base_currency = Currency.objects.get(code=currency_pair[:3].upper())
        target_currency = Currency.objects.get(code=currency_pair[3:].upper())

        try:
            exchange_rate = ExchangeRate.objects.get(
                base_currency=base_currency, target_currency=target_currency
            )
        except ExchangeRate.DoesNotExist:
            return Response(
                {"code": 404, "message": "Валюта не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(exchange_rate)
        return Response(serializer.data)

    def patch(self, request, currency_pair):
        base_currency = Currency.objects.get(code=currency_pair[:3].upper())
        target_currency = Currency.objects.get(code=currency_pair[3:].upper())
        rate_request = float(request.data.get("rate"))

        try:
            exchange_rate = ExchangeRate.objects.get(
                base_currency=base_currency, target_currency=target_currency
            )
        except ExchangeRate.DoesNotExist:
            return Response(
                {"code": 404, "message": "Валюта не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        exchange_rate.rate = rate_request
        exchange_rate.save()

        serializer = self.serializer_class(exchange_rate)

        return Response(serializer.data)

