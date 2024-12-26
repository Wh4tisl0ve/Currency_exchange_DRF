from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

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

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
