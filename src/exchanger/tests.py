from django.urls import include, path, reverse

from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from currencies.models import Currency
from exchange_rates.models import ExchangeRate


class ExchangeRateTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path("api/v1/", include("exchanger.urls")),
    ]

    @classmethod
    def setUpTestData(cls):
        Currency.objects.create(Code="HHH", FullName="DjangoTest", Sign="$")
        test_currency1 = Currency.objects.create(
            Code="TET", FullName="DjangoTest", Sign="$"
        )
        test_currency2 = Currency.objects.create(
            Code="RET", FullName="DjangoTest", Sign="$"
        )
        base = Currency.objects.create(Code="USD", FullName="DjangoTest", Sign="$")
        target = Currency.objects.create(Code="EUR", FullName="DjangoTest", Sign="€")
        ExchangeRate.objects.create(base_currency=base, target_currency=target, rate=5)
        ExchangeRate.objects.create(
            base_currency=base, target_currency=test_currency1, rate=10
        )
        ExchangeRate.objects.create(
            base_currency=base, target_currency=test_currency2, rate=150
        )

    def test_calc_by_direct_rate(self):
        url = reverse("exchanger")
        response = self.client.get(
            url, data={"base": "USD", "target": "EUR", "amount": 5}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("convertedAmount"), "25.0000")

    def test_calc_by_reverse_rate(self):
        url = reverse("exchanger")
        response = self.client.get(
            url, data={"base": "EUR", "target": "USD", "amount": 5}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("convertedAmount"), "1.0000")

    def test_calc_by_reverse_rate(self):
        url = reverse("exchanger")
        response = self.client.get(
            url, data={"base": "TET", "target": "RET", "amount": 85}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("convertedAmount"), "1275.0000")

    def test_currency_not_found(self):
        url = reverse("exchanger")
        response = self.client.get(
            url, data={"base": "GET", "target": "RET", "amount": 85}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(), {"detail": "No Currency matches the given query."}
        )

    def test_exchange_rate_not_found(self):
        url = reverse("exchanger")
        response = self.client.get(
            url, data={"base": "HHH", "target": "EUR", "amount": 85}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(), {"detail": "No ExchangeRate matches the given query."}
        )
