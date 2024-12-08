from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Currency
from .serializers import CurrencySerializer, CurrencyWriteSerializer


class CurrenciesViewSet(viewsets.ModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    lookup_field = 'code'

    def get_serializer_class(self):
        if self.action == "create":
            return CurrencyWriteSerializer
        return self.serializer_class

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, code):
        currency = self.get_object()
        serializer = self.get_serializer(currency)
        return Response(serializer.data)
