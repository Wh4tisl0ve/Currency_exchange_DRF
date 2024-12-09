from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ExchangeRateViewSet


router = DefaultRouter()
router.register(r"exchangeRates", ExchangeRateViewSet, basename="exchange_rates")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "exchangeRate/<str:currency_pair>/",
        ExchangeRateViewSet.as_view({"get": "retrieve", "patch": "update"}),
        name="currency_pair",
    ),
]
