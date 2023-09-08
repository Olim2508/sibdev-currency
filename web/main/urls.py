from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

app_name = 'main'

router = DefaultRouter()
# router.register("user", views.UserMe, basename="user")

urlpatterns = [

]


urlpatterns += router.urls
