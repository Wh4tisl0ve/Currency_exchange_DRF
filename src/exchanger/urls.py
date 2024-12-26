from django.urls import path

from .views import ExchangerView


urlpatterns = [
    path("exchange", ExchangerView.as_view(), name="exchanger"),
]
