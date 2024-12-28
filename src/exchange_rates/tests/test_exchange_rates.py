from django.urls import include, path, reverse

from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from currencies.models import Currency
from ..models import ExchangeRate


class ExchangeRatesTests(APITestCase, URLPatternsTestCase):
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

    def test_get_all_exchange_rates(self):
        url = reverse("exchange_rates")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("base_currency", {}).get("Code"), "USD")
        self.assertEqual(response.data[0].get("target_currency", {}).get("Code"), "EUR")

    def test_get_add_new_exchange_rate(self):
        url = reverse("exchange_rates")
        response = self.client.post(
            url,
            {
                "baseCurrencyCode": "TET",
                "targetCurrencyCode": "RET",
                "rate": 3,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("base_currency", {}).get("Code"), "TET")
        self.assertEqual(response.data.get("target_currency", {}).get("Code"), "RET")

    def test_required_field_missing(self):
        url = reverse("exchange_rates")
        response = self.client.post(
            url,
            {"baseCurrencyCode": "TET"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "targetCurrencyCode": ["Обязательное поле."],
                "rate": ["Обязательное поле."],
            },
        )

    def test_currency_not_exists(self):
        url = reverse("exchange_rates")
        response = self.client.post(
            url,
            {
                "baseCurrencyCode": "TTT",
                "targetCurrencyCode": "RET",
                "rate": 3,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(), {"detail": "No Currency matches the given query."}
        )

    def test_exchange_rate_already_exists(self):
        url = reverse("exchange_rates")
        response = self.client.post(
            url,
            {
                "baseCurrencyCode": "USD",
                "targetCurrencyCode": "EUR",
                "rate": 3,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.json(), {"detail": "Валютная пара с таким кодом уже существует"}
        )
