from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ExchangerView


router = DefaultRouter()
router.register(r"exchange", ExchangerView, basename="exchange_rates")


urlpatterns = [
    path("exchange", ExchangerView.as_view(), name="exchanger"),
]
