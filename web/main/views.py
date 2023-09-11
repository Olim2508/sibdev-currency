from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins, filters
from rest_framework.decorators import action
from rest_framework.pagination import BasePagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.models import ExchangeRateItem
from main.schemas import ordering_rates_parameter
from main.serializers import TrackedCurrencySerializer, RatesSerializer
from main.services import TrackedCurrencyService


class CurrencyViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TrackedCurrencySerializer
    pagination_class = BasePagination

    @swagger_auto_schema(methods=['POST'], request_body=TrackedCurrencySerializer,
                         operation_description="Добавление котируемой валюты \
                          в список отслеживаемых с установкой порогового значения")
    @action(detail=False, methods=['POST'], url_path=r'user_currency', url_name="add_user_currency")
    def add_user_currency(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(methods=['GET'], operation_description="Получение аналитических данных по \
                        котирумой валюте за период")
    @action(detail=False, methods=['GET'], url_path=r'(?P<id>\d+)/analytics', url_name="get_currency_analytics")
    def get_currency_analytics(self, request, id, *args, **kwargs):
        return Response([], status=status.HTTP_200_OK)


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
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


