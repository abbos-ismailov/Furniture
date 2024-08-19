from django.contrib import admin
from .models import Comment, Portfolio

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['name', "owner", "price", "id"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ['writer', "product", "id"]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Portfolio, PortfolioAdmin)