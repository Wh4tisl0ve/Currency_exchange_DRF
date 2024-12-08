from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CurrenciesViewSet


router = DefaultRouter()
router.register(r"currencies", CurrenciesViewSet, basename="currencies")
router.register(r"currency", CurrenciesViewSet, basename="currency")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "currency/<str:currency_code>/",
        CurrenciesViewSet.as_view({"get": "retrive"}),
        name="currency_by_code",
    ),
]
