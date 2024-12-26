from django.urls import path

from .views import CurrencyViewSet


urlpatterns = [
    path(
        "currency/<str:Code>/",
        CurrencyViewSet.as_view({"get": "retrieve"}),
        name="currency_by_code",
    ),
    path(
        "currencies/",
        CurrencyViewSet.as_view({"get": "list", "post": "create"}),
        name="currencies",
    ),
]
