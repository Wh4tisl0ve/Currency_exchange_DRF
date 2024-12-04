from django.urls import path


from .views import ExchangeRatesList, ExchangeRatePairList

urlpatterns = [
    path('exchangeRates/', ExchangeRatesList.as_view(), name='exchange_rates'),
    path('exchangeRates/<str:currency_pair>', ExchangeRatePairList.as_view(), name='exchange_rates')
]