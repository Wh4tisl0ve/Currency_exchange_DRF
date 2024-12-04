from django.urls import path

from .views import CurrenciesList, CurrencyDetail


urlpatterns = [
    path("currencies/", CurrenciesList.as_view(), name="currencies"),
    path("currency/<str:currency_code>", CurrencyDetail.as_view(), name="currency-detail"),
]
