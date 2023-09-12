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


class AnalyticsRatesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateTimeField()
    char_code = serializers.CharField()
    value = serializers.DecimalField(max_digits=10, decimal_places=4)
    is_threshold_exceeded = serializers.BooleanField()
    threshold_match_type = serializers.CharField()
    is_min_value = serializers.BooleanField()
    is_max_value = serializers.BooleanField()
    percentage_ratio = serializers.DecimalField(max_digits=5, decimal_places=2)


