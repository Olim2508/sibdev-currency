import json
import os
from typing import List

import requests
from django.db import transaction

from main.models import Currency, TrackedCurrency, ExchangeRateItem
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

    @staticmethod
    def is_currency_tracked_by_user(user: User, currency: Currency) -> bool:
        return TrackedCurrency.objects.filter(user=user, currency=currency).exists()


class ExchangeRateItemService:

    @staticmethod
    def fetch_and_save_exchange_rate_data(url):
        try:
            data = requests.get(url).json()
        except Exception as e:
            print(f'Ошибка при получении данных: {str(e)}')
            return

        valute_data = data.get('Valute', {})
        date = data.get('Date', '')
        exchange_rate_items = []

        for code, rate_info in valute_data.items():
            exchange_rate_item = ExchangeRateItem(
                currency_id=rate_info.get('ID', ''),
                currency_name=rate_info.get('Name', ''),
                num_code=rate_info.get('NumCode', ''),
                char_code=rate_info.get('CharCode', ''),
                nominal=rate_info.get('Nominal', ''),
                value=rate_info.get('Value', ''),
                previous_rate=rate_info.get('Previous', ''),
                date=date,
            )
            exchange_rate_items.append(exchange_rate_item)

        if exchange_rate_items:
            with transaction.atomic():
                ExchangeRateItem.objects.bulk_create(exchange_rate_items)

            print(f'Записи о курсах созданы успешно - {date}')

