from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'main'

router = DefaultRouter()
router.register("currency", views.CurrencyViewSet, basename="currency")
router.register("rates", views.RatesViewSet, basename="rates")

urlpatterns = [
    path("available-currencies/list", views.CurrencyListViewSet.as_view({"get": "list"}), name="currency-list"),
]


urlpatterns += router.urls
