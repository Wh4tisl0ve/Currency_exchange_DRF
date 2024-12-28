from django.urls import include, path, reverse

from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from currencies.models import Currency
from ..models import ExchangeRate


class ExchangeRateTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path("api/v1/", include("exchange_rates.urls")),
    ]

    @classmethod
    def setUpTestData(cls):
        Currency.objects.create(Code="TET", FullName="DjangoTest", Sign="$")
        Currency.objects.create(Code="RET", FullName="DjangoTest", Sign="$")
        base = Currency.objects.create(Code="USD", FullName="DjangoTest", Sign="$")
        target = Currency.objects.create(Code="EUR", FullName="DjangoTest", Sign="€")
        ExchangeRate.objects.create(base_currency=base, target_currency=target, rate=5)

    def test_get_concrete_exchange_rate(self):
        url = reverse(
            "exchange_rate_by_currency_pair", kwargs={"currency_pair": "USDEUR"}
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("base_currency", {}).get("Code"), "USD")
        self.assertEqual(response.data.get("target_currency", {}).get("Code"), "EUR")

    def test_currency_not_found(self):
        url = reverse(
            "exchange_rate_by_currency_pair", kwargs={"currency_pair": "YEYEUR"}
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(),
            {"detail": "No Currency matches the given query."},
        )

    def test_update_exchange_rate(self):
        url = reverse(
            "exchange_rate_by_currency_pair", kwargs={"currency_pair": "USDEUR"}
        )
        response = self.client.patch(url, {"rate": 5.2501}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("rate"), "5.2501")

    def test_update_exchange_rate_invalid_field(self):
        url = reverse(
            "exchange_rate_by_currency_pair", kwargs={"currency_pair": "USDEUR"}
        )
        response = self.client.patch(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"non_field_errors": ["Отсутствует нужное поле формы"]}
        )

    def test_update_exchange_rate_not_found(self):
        url = reverse(
            "exchange_rate_by_currency_pair", kwargs={"currency_pair": "USDTET"}
        )
        response = self.client.patch(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(), {"detail": "No ExchangeRate matches the given query."}
        )
