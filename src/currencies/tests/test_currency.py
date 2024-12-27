from django.urls import include, path, reverse

from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from ..models import Currency


class CurrencyTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path("api/v1/", include("currencies.urls")),
    ]

    @classmethod
    def setUpTestData(cls):
        Currency.objects.create(Code="USD", FullName="DjangoTest", Sign="$")

    def test_get_concrete_currency(self):
        url = reverse("currency_by_code", kwargs={"Code": "USD"})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("Code"), "USD")

    def test_incorrect_format_code(self):
        url = reverse("currency_by_code", kwargs={"Code": "123"})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"Code": {"detail": "Неверный формат поля code"}},
        )

    def test_currency_not_exists(self):
        url = reverse("currency_by_code", kwargs={"Code": "QQQ"})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data,
            {"detail": "No Currency matches the given query."},
        )