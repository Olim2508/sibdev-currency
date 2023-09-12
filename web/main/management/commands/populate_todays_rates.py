from django.core.management.base import BaseCommand
from main.services import ExchangeRateItemService


class Command(BaseCommand):
    help = 'Загрузка котировок в БД за текущий день'

    def handle(self, *args, **kwargs):
        current_date_url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        ExchangeRateItemService.fetch_and_save_exchange_rate_data(current_date_url)

