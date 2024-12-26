from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from currencies.models import Currency
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer, ExchangeRateWriteSerializer


class ExchangeRateViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = ExchangeRateSerializer
    queryset = ExchangeRate.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ExchangeRateWriteSerializer
        return self.serializer_class

    def retrieve(self, request, currency_pair):
        exchange_rate = self.get_object(currency_pair)
        serializer = self.get_serializer(exchange_rate)

        return Response(serializer.data)

    def update(self, request, currency_pair):
        exchange_rate = self.get_object(currency_pair)
        serializer = self.get_serializer(exchange_rate, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def get_object(self, currency_pair: str) -> ExchangeRate:
        base_currency = get_object_or_404(Currency, Code=currency_pair[:3].upper())
        target_currency = get_object_or_404(Currency, Code=currency_pair[3:].upper())

        exchange_rate = get_object_or_404(
            ExchangeRate, base_currency=base_currency, target_currency=target_currency
        )

        return exchange_rate
