from rest_framework import serializers

from .models import Currency, TrackedCurrency
from .services import TrackedCurrencyService


class TrackedCurrencySerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        TrackedCurrencyService.create_tracked_currency(user=self.context['request'].user, **self.validated_data)

    class Meta:
        model = TrackedCurrency
        exclude = ("user",)

