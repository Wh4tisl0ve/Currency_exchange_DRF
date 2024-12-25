from django.db import IntegrityError

from rest_framework import mixins, status
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

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except IntegrityError:
            return Response(
                {"message": "Валюта с таким кодом уже существует"},
                status=status.HTTP_409_CONFLICT,
            )
