from django.db import IntegrityError

from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from .models import Currency
from .serializers import CurrencySerializer, CurrencyWriteSerializer


class CurrencyViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    lookup_url_kwarg = "Code"
    lookup_field = "Code__iexact"

    def get_serializer_class(self):
        if self.action == "create":
            return CurrencyWriteSerializer
        return self.serializer_class

    @extend_schema(
        summary="Получение списка валют",
        description="Возвращает список всех валют, находящихся в базе данных",
        responses={
            200: CurrencySerializer,
        },
    )
    def list(self, request):
        return super().list(request)

    @extend_schema(
        summary="Добавление новой валюты в базу",
        description="Данные передаются в теле запроса в виде полей формы (x-www-form-urlencoded). Поля формы - name, code, sign",
        request=CurrencyWriteSerializer,
        responses={
            201: CurrencySerializer,
            400: OpenApiResponse(description="Отсутствует нужное поле формы"),
            409: OpenApiResponse(description="Валюта с таким кодом уже существует"),
        },
    )
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"message": "Валюта с таким кодом уже существует"},
                status=status.HTTP_409_CONFLICT,
            )

    @extend_schema(
        summary="Получение конкретной валюты",
        description="Получение конкретной валюты по коду. Код должен состоять из 3 латинских букв",
        request=CurrencyWriteSerializer,
        responses={
            201: CurrencySerializer,
            400: OpenApiResponse(description="Неверный формат кода валюты"),
            404: OpenApiResponse(description="Валюта не найдена"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
