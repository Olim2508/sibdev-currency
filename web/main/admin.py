from django.contrib import admin
from .models import ExchangeRateItem


@admin.register(ExchangeRateItem)
class ExchangeRateItemAdmin(admin.ModelAdmin):
    list_display = (
        'currency_id',
        'currency_name',
        'num_code',
        'char_code',
        'nominal',
        'exchange_rate',
        'previous_rate',
        'date',
    )
    list_filter = (
        'currency_name',
    )
