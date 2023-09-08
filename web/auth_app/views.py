from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from . import serializers
from dj_rest_auth import views as auth_views

from .schemas import logout_body_scheme
from .serializers import UserMeSerializers

User = get_user_model()


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = serializers.SignUpSerializer


class LogInView(auth_views.LoginView):
    serializer_class = serializers.LogInSerializer


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=logout_body_scheme
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserMe(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['GET'], url_path=r'me',
            serializer_class=UserMeSerializers, url_name="user_me")
    def user_me(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
