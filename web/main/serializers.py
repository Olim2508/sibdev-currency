from rest_framework import serializers

from .models import TrackedCurrency, ExchangeRateItem
from .services import TrackedCurrencyService


class TrackedCurrencySerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        TrackedCurrencyService.create_tracked_currency(user=self.context['request'].user, **self.validated_data)

    class Meta:
        model = TrackedCurrency
        exclude = ("user",)


class RatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeRateItem
        fields = ["id", "date", "char_code", "value"]

