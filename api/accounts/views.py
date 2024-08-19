from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    SignUpSerializer,
    LoginSerializer,
    LogoutSerializer,
    UpdateAccessTokenSerizlizer,
)


class CreateUserApiView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer


class LoginApiView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)


class LogoutApiView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {"status": True, "message": "Siz tizimdan chiqdingiz..."}
            return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            data = {"status": False, "message": f"{e}"}
            return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UpdateAccessTokenApiView(TokenRefreshView):
    serializer_class = UpdateAccessTokenSerizlizer
