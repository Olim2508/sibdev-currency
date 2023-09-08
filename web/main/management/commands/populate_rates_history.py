import requests
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from main.models import ExchangeRateItem


class Command(BaseCommand):
    help = 'Загрузка истории котировок в БД за последние 30 дней, включая текущий день'

    def handle(self, *args, **kwargs):
        current_date_url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        current_day_data = self.get_exchange_rate_data(current_date_url)
        if current_day_data:
            self.save_exchange_rate_data(current_day_data)

        base_url = 'https://www.cbr-xml-daily.ru/archive/'
        today = datetime.now()

        for day in range(1, 31):
            date = today - timedelta(days=day)
            formatted_date = date.strftime('%Y/%m/%d')
            previous_day_url = f'{base_url}{formatted_date}/daily_json.js'

            previous_day_data = self.get_exchange_rate_data(previous_day_url)
            if previous_day_data:
                self.save_exchange_rate_data(previous_day_data)

    def get_exchange_rate_data(self, url):
        try:
            return requests.get(url).json()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка при загрузке данных: {str(e)}'))
            return None

    def save_exchange_rate_data(self, data):
        valute_data = data.get('Valute', {})
        date = data.get('Date', '')

        for code, rate_info in valute_data.items():
            ExchangeRateItem.objects.create(
                currency_id=rate_info.get('ID', ''),
                currency_name=rate_info.get('Name', ''),
                num_code=rate_info.get('NumCode', ''),
                char_code=rate_info.get('CharCode', ''),
                nominal=rate_info.get('Nominal', ''),
                exchange_rate=rate_info.get('Value', ''),
                previous_rate=rate_info.get('Previous', ''),
                date=date,
            )

            self.stdout.write(self.style.SUCCESS(
                f'Запись о курсе создана успешно для {rate_info.get("CharCode", "")} - {date}')
            )
