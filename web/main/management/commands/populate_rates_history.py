from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from main.services import ExchangeRateItemService


class Command(BaseCommand):
    help = 'Загрузка истории котировок в БД за последние 30 дней, включая текущий день'

    def handle(self, *args, **kwargs):
        current_date_url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        ExchangeRateItemService.fetch_and_save_exchange_rate_data(current_date_url)

        base_url = 'https://www.cbr-xml-daily.ru/archive/'
        today = datetime.now()

        for day in range(1, 31):
            date = today - timedelta(days=day)
            formatted_date = date.strftime('%Y/%m/%d')
            previous_day_url = f'{base_url}{formatted_date}/daily_json.js'

            ExchangeRateItemService.fetch_and_save_exchange_rate_data(previous_day_url)
