from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from drf_spectacular.utils import extend_schema, OpenApiResponse

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

    @extend_schema(
        summary="Получение списка всех обменных курсов",
        description="Возвращает список всех обменных курсов, находящихся в базе данных",
        responses={
            200: ExchangeRateSerializer,
        },
    )
    def list(self, request):
        return super().list(request)

    @extend_schema(
        summary="Добавление нового обменного курса в базу",
        description="Данные передаются в теле запроса в виде полей формы (x-www-form-urlencoded). Поля формы - baseCurrencyCode, targetCurrencyCode, rate",
        request=ExchangeRateWriteSerializer,
        responses={
            201: ExchangeRateSerializer,
            400: OpenApiResponse(description="Отсутствует нужное поле формы"),
            404: OpenApiResponse(
                description="Одна(или обе) валюта из валютной пары не существует в БД"
            ),
            409: OpenApiResponse(
                description="Валютная пара с таким кодом уже существует"
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение конкретного обменного курса",
        description="Валютная пара задаётся идущими подряд кодами валют в адресе запроса",
        responses={
            200: ExchangeRateSerializer,
            404: OpenApiResponse(
                description="Валюта или обменный курс для пары не найден"
            ),
        },
    )
    def retrieve(self, request, currency_pair):
        exchange_rate = self.get_object(currency_pair)
        serializer = self.get_serializer(exchange_rate)

        return Response(serializer.data)

    @extend_schema(
        summary="Обновление существующего в базе обменного курса",
        description="Валютная пара задаётся идущими подряд кодами валют в адресе запроса. Данные передаются в теле запроса в виде полей формы (x-www-form-urlencoded). Единственное поле формы - rate",
        responses={
            200: ExchangeRateSerializer,
            400: OpenApiResponse(description="Отсутствует нужное поле формы"),
            404: OpenApiResponse(
                description="Валюта или обменный курс для пары не найден"
            ),
        },
    )
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
