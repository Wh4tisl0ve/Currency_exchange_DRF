from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CurrencyViewSet


router = DefaultRouter()
router.register(r"currencies", CurrencyViewSet, basename="currencies")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "currency/<str:Code>/",
        CurrencyViewSet.as_view({"get": "retrieve"}),
        name="currency_by_code",
    ),
]
