from django.urls import path, include


urlpatterns = [
    path("api/", include("currencies.urls")),
    path("api/", include("exchange_rates.urls")),
]
