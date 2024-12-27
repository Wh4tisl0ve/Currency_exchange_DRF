from django.urls import include, path, reverse

from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from ..models import Currency


class CurrenciesTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path("api/v1/", include("currencies.urls")),
    ]

    @classmethod
    def setUpTestData(cls):
        Currency.objects.create(Code="USD", FullName="DjangoTest", Sign="$")
        Currency.objects.create(Code="EUR", FullName="DjangoTest", Sign="€")

    def test_get_all_currencies(self):
        url = reverse("currencies")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data[0],
            {"id": 1, "Code": "USD", "FullName": "DjangoTest", "Sign": "$"},
        )

    def test_add_not_exists_currency(self):
        url = reverse("currencies")
        response = self.client.post(
            url,
            {"Code": "NEW", "FullName": "DjangoTest", "Sign": "$"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("Code"), "NEW")

    def test_add_exists_currency(self):
        url = reverse("currencies")
        response = self.client.post(
            url,
            {"Code": "USD", "FullName": "DjangoTest", "Sign": "$"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.json(), {"message": "Валюта с таким кодом уже существует"}
        )

    def test_required_field_missing(self):
        url = reverse("currencies")
        response = self.client.post(
            url,
            {"Code": "CUR"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"FullName": ["Обязательное поле."], "Sign": ["Обязательное поле."]},
        )
