from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ExchangeRateItem(models.Model):
    currency_id = models.CharField(max_length=255)
    currency_name = models.CharField(max_length=255)
    num_code = models.CharField(max_length=255)
    char_code = models.CharField(max_length=255)
    nominal = models.IntegerField()
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    previous_rate = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.currency_name} - {self.date.strftime('%Y/%m/%d')} - {self.exchange_rate}"


class Currency(models.Model):
    char_code = models.CharField(max_length=255)
    currency_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.char_code} - {self.currency_name}"

    class Meta:
        verbose_name = "Котируемая валюта"
        verbose_name_plural = "Котируемые валюты"


class TrackedCurrency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tracked_currencies")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="tracked_currencies")
    threshold = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        verbose_name = "Отслеживаемая КВ"
        verbose_name_plural = "Отслеживаемые КВ"
