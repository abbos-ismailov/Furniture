from django.db import models
from api.base.models import BaseModel
from api.accounts.models import User
from django.core.validators import FileExtensionValidator


class Portfolio(BaseModel):
    name = models.CharField(max_length=150)
    img = models.ImageField(
        upload_to="photo/portfolios",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "heic", "heif", "webp"]
            )
        ],
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="portfolio_user"
    )
    price = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.owner} made {self.name}"


class Comment(BaseModel):
    product = models.ForeignKey(
        Portfolio,
        on_delete=models.SET_NULL,
        related_name="comment_portfolio",
        null=True,
    )
    text = models.CharField(max_length=650)
    writer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="comment_writer", null=True
    )

    def __str__(self) -> str:
        return f"{self.writer} wrote {self.text[:9]}"