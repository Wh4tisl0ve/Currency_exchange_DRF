from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ExchangeRateViewSet


router = DefaultRouter()
router.register(r"exchangeRates", ExchangeRateViewSet, basename="exchange_rates")

urlpatterns = [path("", include(router.urls))]
