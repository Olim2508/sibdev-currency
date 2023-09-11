from django.contrib import admin
from .models import ExchangeRateItem, Currency, TrackedCurrency


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


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'currency_name',
        'char_code',
    )


@admin.register(TrackedCurrency)
class TrackedCurrencyAdmin(admin.ModelAdmin):
    list_display = (
        'currency',
        'user',
        'threshold',
    )
