from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/accounts/", include("api.accounts.urls")),
    path("api/v1/home/", include("api.home.urls")),
]

urlpatterns += [
    # your other URL patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)