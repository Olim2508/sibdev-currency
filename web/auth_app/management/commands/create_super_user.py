from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Создать суперпользователь, если он не существует'

    def handle(self, *args, **options):
        user = {
            "email": settings.SUPERUSER_EMAIL,
            "password": make_password(settings.SUPERUSER_PASSWORD),
        }

        if not User.objects.filter(email=user['email'], is_superuser=True).exists():
            User.objects.create(
                is_active=True,
                is_staff=True,
                is_superuser=True,
                **user,
            )
            self.stdout.write(self.style.SUCCESS(f'пользователь {user["email"]} успешно создан.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'пользователь {user["email"]} уже существует'))
