from rest_framework import viewsets
from rest_framework.response import Response

from currencies.models import Currency
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer


class ExchangeRateViewSet(viewsets.ModelViewSet):
    serializer_class = ExchangeRateSerializer
    queryset = ExchangeRate.objects.all()

    def get_serializer_class(self):
        return super().get_serializer_class()

    def list(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data)

    def create(self, request):
        pass
