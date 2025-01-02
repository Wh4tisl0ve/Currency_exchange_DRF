from django.urls import re_path

from .views import ExchangerView


urlpatterns = [
    re_path(r"^exchange$", ExchangerView.as_view(), name="exchanger"),
]
