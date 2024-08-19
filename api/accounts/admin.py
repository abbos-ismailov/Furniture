from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', "phone", "email", "id"]
admin.site.register(User, UserAdmin)