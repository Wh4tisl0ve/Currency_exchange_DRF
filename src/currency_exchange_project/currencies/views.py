from django.db import DatabaseError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException

from .models import Currency
from .serializers import CurrencySerializers


class CurrenciesList(APIView):
    serializer_class = CurrencySerializers

    def get(self, request):
        try:
            currencies = Currency.objects.all()
            serializer = self.serializer_class(currencies, many=True)

            return Response(serializer.data)
        except DatabaseError:
            raise APIException("Внутренняя ошибка сервера")

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrencyDetail(APIView):
    serializer_class = CurrencySerializers

    def get(self, request, currency_code):
        serializer = self.serializer_class(data={"code": currency_code})
        try:
            serializer.is_valid(raise_exception=True)
            currency = Currency.objects.get(code=currency_code)
        except serializers.ValidationError:
            raise APIException("Неверный формат кода валюты")
        except Currency.DoesNotExist:
            raise NotFound("Валюта с данным кодом не найдена")
        except DatabaseError:
            raise APIException("Внутренняя ошибка сервера")

        serializer = self.serializer_class(currency)
        return Response(serializer.data)
