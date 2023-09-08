from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

app_name = 'auth_app'

router = DefaultRouter()
# router.register("user", views.UserMe, basename="user")

urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('log-out/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


urlpatterns += router.urls
