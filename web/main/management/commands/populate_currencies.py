from django.core.management.base import BaseCommand
from main.models import Currency
from main.services import CurrencyService


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        if Currency.objects.count() > 0:
            return
        CurrencyService.populate_currencies()

        self.stdout.write(self.style.SUCCESS(
            f'Котируемые валюты успешно импортированы в базу данных.'
        ))


