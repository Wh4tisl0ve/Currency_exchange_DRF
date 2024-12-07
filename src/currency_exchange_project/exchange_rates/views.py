from django.db.utils import DatabaseError
from django.db.utils import IntegrityError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, NotFound, ParseError

from currencies.models import Currency
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer


class ExchangeRatesList(APIView):
    def get(self, request):
        try:
            exchange_rates = ExchangeRate.objects.all()
            serializer = ExchangeRateSerializer(exchange_rates, many=True)
            return Response(serializer.data)
        except DatabaseError:
            raise APIException("Внутренняя ошибка сервера")

    def post(self, request):
        serializer = ExchangeRateSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            exchange_rate = serializer.save()
            
            serializer = ExchangeRateSerializer(exchange_rate)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"detail": "Обменный курс с валютной парой уже существует"},
                status=status.HTTP_409_CONFLICT,
            )
        except DatabaseError:
            raise APIException("Внутренняя ошибка сервера")


class ExchangeRatePairDetail(APIView):
    def get(self, request, currency_pair):
        try:
            base_currency = Currency.objects.get(code=currency_pair[:3].upper())
            target_currency = Currency.objects.get(code=currency_pair[3:].upper())

            exchange_rate = ExchangeRate.objects.get(
                base_currency=base_currency,
                target_currency=target_currency,
            )
            serializer = ExchangeRateSerializer(exchange_rate)

            return Response(serializer.data)
        except Currency.DoesNotExist:
            raise ParseError("Одна из валют валютной пары не существует")
        except ExchangeRate.DoesNotExist:
            raise NotFound("Обменного курса для валютной пары не найдено")
        except DatabaseError:
            raise APIException("Внутренняя ошибка сервера")
