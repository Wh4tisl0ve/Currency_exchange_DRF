from django.db import models
from currencies.models import Currency


class ExchangeRate(models.Model):
    base_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="base_currency",
    )
    target_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="target_currency",
    )
    rate = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["base_currency", "target_currency"],
                name="unique_currencies_pair",
            ),
        ]
        indexes = [
            models.Index(
                fields=["base_currency", "target_currency"],
                name="index_currencies_pair",
            ),
        ]

    def __str__(self):
        return f"{self.base_currency} - {self.target_currency}"
