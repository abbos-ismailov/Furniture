from django.db import models
from django.contrib.auth.models import AbstractUser
from api.base.models import BaseModel
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken


CONSUMER, MASTER, DESIGNER = ("consumer", "master", "designer")
USER_ROLES = ((CONSUMER, CONSUMER), (MASTER, MASTER), (DESIGNER, DESIGNER))


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True, null=True, blank=True)
    avatar = models.ImageField(
        upload_to="photo/user",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "heic", "heif", "webp"]
            )
        ],
    )
    phone = models.CharField(max_length=15, null=True, unique=True)
    user_roles = models.CharField(max_length=40, choices=USER_ROLES, default=CONSUMER)
    link = models.CharField(max_length=150, null=True, blank=True)
    job = models.CharField(max_length=150, null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}
