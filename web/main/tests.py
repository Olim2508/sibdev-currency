from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import tag
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from main.models import Currency, TrackedCurrency, ExchangeRateItem
from main.services import CurrencyService

User = get_user_model()


@tag('tracked-currency')
class TrackedCurrencyTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        data = {
            'email': 'john@gmail.com',
            'password': make_password('john123456')
        }
        cls.user = User.objects.create(**data, is_active=True)
        CurrencyService.populate_currencies()

    def setUp(self):
        url = reverse_lazy('auth_app:login')
        data = {
            'email': self.user.email,
            "password": "john123456"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access_token"]}')

    def test_add_user_currency(self):
        url = reverse_lazy('main:currency-add_user_currency')
        data = {
            "currency": 100,
            "threshold": 100
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        currency = Currency.objects.filter(char_code="USD").first()
        data["currency"] = currency.id
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertTrue(TrackedCurrency.objects.filter(currency=currency, user=self.user).exists())


@tag('rates')
class RatesTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        data = {
            'email': 'john@gmail.com',
            'password': make_password('john123456')
        }
        cls.user = User.objects.create(**data, is_active=True)
        CurrencyService.populate_currencies()
        cls.rate_item_1 = ExchangeRateItem.objects.create(
            currency_id="R01090B",
            currency_name="Белорусский рубль",
            num_code="933",
            char_code="BYN",
            nominal=1,
            value=29.8759,
            previous_rate=29.9159,
            date="2023-09-09T11:30:00+03:00",
        )
        cls.rate_item_2 = ExchangeRateItem.objects.create(
            currency_id="R01035",
            currency_name="Фунт стерлингов Соединенного королевства",
            num_code="826",
            char_code="GBP",
            nominal=1,
            value=122.1701,
            previous_rate=122.6567,
            date="2023-09-09T11:30:00+03:00",
        )
        currency = Currency.objects.filter(char_code="GBP").first()
        cls.tracked_currency = TrackedCurrency.objects.create(user=cls.user, currency=currency, threshold=10)

    def setUp(self):
        url = reverse_lazy('auth_app:login')
        data = {
            'email': self.user.email,
            "password": "john123456"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access_token"]}')

    def test_get_rates_for_registered_user(self):
        url = reverse_lazy('main:rates-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['char_code'], self.tracked_currency.currency.char_code)

    def test_get_rates_for_anonymous_user(self):
        url = reverse_lazy('main:rates-list')
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 2)

