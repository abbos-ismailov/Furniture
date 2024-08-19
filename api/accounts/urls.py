from django.urls import path
from .views import CreateUserApiView, LoginApiView, LogoutApiView, UpdateAccessTokenApiView


urlpatterns = [
    path("signup/", CreateUserApiView.as_view()),
    path("login/", LoginApiView.as_view()),
    path('logout/', LogoutApiView.as_view()),
    path('update-access/', UpdateAccessTokenApiView.as_view()),
]
