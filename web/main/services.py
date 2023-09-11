import json
import os
from typing import List

from main.models import Currency, TrackedCurrency
from django.contrib.auth import get_user_model


User = get_user_model()


class CurrencyService:

    @staticmethod
    def populate_currencies() -> None:
        file_path = os.path.join(os.path.dirname(__file__) + "/data/currencies.json")

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        currencies_to_create = [
            Currency(char_code=entry['char_code'], currency_name=entry['currency_name'])
            for entry in data
        ]
        Currency.objects.bulk_create(currencies_to_create)


class TrackedCurrencyService:

    @staticmethod
    def create_tracked_currency(**data):
        return TrackedCurrency.objects.create(**data)

    @staticmethod
    def get_user_tracked_currencies_code_list(user: User) -> List[int]:
        return TrackedCurrency.objects.filter(user=user).values_list("currency__char_code")
