from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import tag
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from main.models import Currency, TrackedCurrency
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

