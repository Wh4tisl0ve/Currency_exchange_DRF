from django.db import DatabaseError
from django.db.utils import IntegrityError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException

from .models import Currency
from .serializers import CurrencyReadSerializer, CurrencyWriteSerializer


class CurrenciesList(APIView):
    def get(self, request):
        try:
            currencies = Currency.objects.all()
            serializer = CurrencyReadSerializer(currencies, many=True)

            return Response(serializer.data)
        except DatabaseError:
            raise APIException("Внутренняя ошибка сервера")

    def post(self, request):
        serializer = CurrencyWriteSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            currency = serializer.save()
            serializer = CurrencyWriteSerializer(currency)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"detail": "Валюта с таким кодом уже существует"},
                status=status.HTTP_409_CONFLICT,
            )


class CurrencyDetail(APIView):
    def get(self, request, currency_code):
        serializer = CurrencyReadSerializer(data={"code": currency_code.upper()})
        try:
            serializer.is_valid(raise_exception=True)
            currency = Currency.objects.get(code=currency_code.upper())
        except Currency.DoesNotExist:
            raise NotFound("Валюта с данным кодом не найдена")
        except DatabaseError:
            raise APIException("Внутренняя ошибка сервера")

        serializer = CurrencyReadSerializer(currency)
        return Response(serializer.data)
