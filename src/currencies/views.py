from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

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
    lookup_field = "Code"

    def get_serializer_class(self):
        if self.action == "create":
            return CurrencyWriteSerializer
        return self.serializer_class
