from decimal import Decimal

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from currencies.models import Currency
from .service import ExchangerService
from exchanger.serializers import (
    ExchangerResponseSerializer,
    ExchangerRequestSerializer,
)


class ExchangerView(APIView):
    @extend_schema(
        summary="Расчёт перевода определённого количества средств из одной валюты в другую",
        description="Обязательные параметры - base, target, amount",
        parameters=[
            OpenApiParameter(name="base", description="Базовая валюта", type=str),
            OpenApiParameter(name="target", description="Целевая валюта", type=str),
            OpenApiParameter(name="amount", description="Количество", type=Decimal),
        ],
        responses={
            200: ExchangerResponseSerializer,
            400: OpenApiResponse(description="Отсутствует нужный параметр"),
            404: OpenApiResponse(
                description="Валюта или обменный курс для пары не найден"
            ),
        },
    )
    def get(self, request):
        serializer_request = ExchangerRequestSerializer(data=request.query_params)
        serializer_request.is_valid(raise_exception=True)

        base_currency = get_object_or_404(
            Currency, code=request.query_params.get("base").upper()
        )
        target_currency = get_object_or_404(
            Currency, code=request.query_params.get("target").upper()
        )


        rate_dto = ExchangerService.perform_currency_exchange(
            base_currency, target_currency, request.query_params.get("amount")
        )

        serializer_response = ExchangerResponseSerializer(rate_dto)

        return Response(serializer_response.data)
