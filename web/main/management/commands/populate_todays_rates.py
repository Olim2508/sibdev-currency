import requests
from django.core.management.base import BaseCommand
from main.models import ExchangeRateItem


class Command(BaseCommand):
    help = 'Загрузка котировок в БД за текущий день'

    def handle(self, *args, **kwargs):
        current_date_url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        current_day_data = self.get_exchange_rate_data(current_date_url)
        if current_day_data:
            self.save_exchange_rate_data(current_day_data)

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
