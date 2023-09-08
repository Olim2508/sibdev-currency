from django.db import models


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
