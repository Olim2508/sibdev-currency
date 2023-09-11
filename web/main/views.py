from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.pagination import BasePagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.serializers import TrackedCurrencySerializer


class TrackedCurrencyViewSet(mixins.CreateModelMixin,
                             GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TrackedCurrencySerializer


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
