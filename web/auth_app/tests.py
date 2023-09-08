from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import tag
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

User = get_user_model()


@tag('user')
class UserTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        data = {
            'email': 'john@gmail.com',
            'password': make_password('john123456')
        }
        cls.user = User.objects.create(**data, is_active=True)

    def test_register_user(self):
        url = reverse_lazy('auth_app:register')
        data = {
            "email": "test@gmail.com",
            "password1": "admin123456",
            "password2": "admin123456",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_login(self):
        url = reverse_lazy('auth_app:login')
        data = {
            'email': "not_exists@gmail.com",
            "password": "john123456"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        data['email'] = self.user.email
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
