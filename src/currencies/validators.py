from rest_framework import serializers


class CurrencyCodeValidators:
    def __call__(self, value: str):
        if not self.is_currency_code(value):
            raise serializers.ValidationError({"detail": "Неверный формат поля code"})

        return value

    def is_currency_code(self, value: str) -> bool:
        return len(value) == 3 and value.isalpha() and value.isascii()
