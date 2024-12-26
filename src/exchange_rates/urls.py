from django.urls import path

from .views import ExchangeRateViewSet


urlpatterns = [
    path(
        "exchangeRates/",
        ExchangeRateViewSet.as_view({"get": "list", "post": "create"}),
        name="exchange_rates",
    ),
    path(
        "exchangeRate/<str:currency_pair>/",
        ExchangeRateViewSet.as_view({"get": "retrieve", "patch": "update"}),
        name="exchange_rate_by_currency_pair",
    ),
]
