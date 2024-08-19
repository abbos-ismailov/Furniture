from rest_framework import exceptions, serializers, generics
from .models import User
from api.base.utility import check_username
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt import tokens
from rest_framework.exceptions import ValidationError
from django.contrib.auth import models
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "username",
            "avatar",
            "user_roles",
            "link",
            "job",
            "password",
            "confirm_password",
        )

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user

    def validate_username(self, username):
        if check_username(username) == False:
            raise exceptions.ValidationError(
                {"message": "Username must be between 3 and 35 characters"}
            )
        if User.objects.filter(username=username).exists():
            raise exceptions.ValidationError(
                {"message": "Bu username allaqachon olingan"}
            )

        return username

    def validate(self, data):
        password = data.get("password", None)
        confirm_password = data.get("confirm_password", None)
        if password != confirm_password:
            raise exceptions.ValidationError(
                {
                    "status": False,
                    "message": "Parollar bir biriga teng bo'lishi kerak !!!",
                }
            )
        if password:
            validate_password(password=password)
        return data

    def to_representation(self, instance):
        response_data = {
            "access": instance.token().get("access"),
            "refresh": instance.token().get("refresh"),
            "message": "User registered successfully!",
        }
        return response_data


class LoginSerializer(TokenObtainPairSerializer):
    def auth_validate(self, data):
        username = data.get("username")
        password = data.get("password")
        auth_kwargs = {self.username_field: username, "password": password}
        user = authenticate(**auth_kwargs)

        if user:
            self.user = user
        else:
            # self.trying_count += 1
            data = {
                "status": False,
                "message": "Username or password is wrong !!!",
            }
            raise ValidationError(data)

    def validate(self, data):
        self.auth_validate(data=data)
        data = self.user.token()
        data["full_name"] = f"{self.user.first_name} {self.user.last_name}"
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UpdateAccessTokenSerizlizer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        access_token_instance = tokens.AccessToken(data["access"])
        user_id = access_token_instance["user_id"]
        user = generics.get_object_or_404(User, pk=user_id)
        models.update_last_login(None, user=user)
        return data
