from django.urls import path

from .views import ExchangeRatesList, ExchangeRatePairDetail

urlpatterns = [
    path('exchangeRates/', ExchangeRatesList.as_view(), name='exchange_rates'),
    path('exchangeRate/<str:currency_pair>', ExchangeRatePairDetail.as_view(), name='exchange_rates')
]