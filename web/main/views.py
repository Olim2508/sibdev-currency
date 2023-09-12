from decimal import Decimal

from django.db.models import Case, When, Value, BooleanField, CharField, F, ExpressionWrapper, DecimalField, Max, Min
from django.db.models.functions import Abs, Cast
from django.shortcuts import get_object_or_404

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins, filters
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.models import ExchangeRateItem, Currency
from main.paginators import BasePagination
from main.schemas import ordering_rates_parameter
from main.serializers import TrackedCurrencySerializer, RatesSerializer, AnalyticsRatesSerializer
from main.services import TrackedCurrencyService


class CurrencyViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = BasePagination

    def get_queryset(self):
        return ExchangeRateItem.objects.order_by("-date")

    @swagger_auto_schema(methods=['POST'], request_body=TrackedCurrencySerializer,
                         operation_description="Добавление котируемой валюты \
                          в список отслеживаемых с установкой порогового значения")
    @action(detail=False, methods=['POST'], url_path=r'user_currency', url_name="add_user_currency")
    def add_user_currency(self, request, *args, **kwargs):
        serializer = TrackedCurrencySerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(methods=['GET'], operation_description="Получение аналитических данных по \
                        котирумой валюте за период")
    @action(detail=False, methods=['GET'], url_path=r'(?P<id>\d+)/analytics', url_name="get_currency_analytics")
    def get_currency_analytics(self, request, id, *args, **kwargs):
        currency = get_object_or_404(Currency, id=id)
        if not TrackedCurrencyService.is_currency_tracked_by_user(user=request.user, currency=currency):
            message = "эта КВ не отслеживается этим пользователем"
            return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.filter_queryset(self.get_queryset().filter(char_code=currency.char_code))

        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if date_from:
            queryset = queryset.filter(date__gte=date_from)

        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        threshold = request.query_params.get('threshold')
        if threshold is None:
            raise ParseError("Параметр 'threshold' обязателен")

        threshold = Decimal(threshold)
        max_value = queryset.aggregate(Max('value'))['value__max']
        min_value = queryset.aggregate(Min('value'))['value__min']

        queryset = queryset.annotate(
            is_threshold_exceeded=Case(
                When(value__lt=threshold, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            threshold_match_type=Case(
                When(value__lt=threshold, then=Value("greater")),
                When(value__gt=threshold, then=Value("less")),
                default=Value("equal"),
                output_field=CharField()
            ),
            is_max_value=Case(
                When(value=F('value') == max_value, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            is_min_value=Case(
                When(value=F('value') == min_value, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            percentage_ratio=ExpressionWrapper(
                Cast(Abs(F('value') - threshold) / F('value') * 100, DecimalField(max_digits=5, decimal_places=2)),
                output_field=DecimalField(max_digits=5, decimal_places=2)
            )
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AnalyticsRatesSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AnalyticsRatesSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RatesViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = RatesSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["value"]

    def get_queryset(self):
        queryset = ExchangeRateItem.objects.all()
        if self.request.user.is_authenticated:
            tracked_currencies_list = TrackedCurrencyService.get_user_tracked_currencies_code_list(self.request.user)
            queryset = queryset.filter(char_code__in=tracked_currencies_list)
            return queryset
        return queryset

    @swagger_auto_schema(manual_parameters=[ordering_rates_parameter])
    # @method_decorator(cache_page(60 * 15))  # кэшировать на 15 минут
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


