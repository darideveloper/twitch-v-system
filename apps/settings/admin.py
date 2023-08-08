from django.contrib import admin
from settings import models

@admin.register(models.Token)
class TokenAdmin (admin.ModelAdmin):
    list_display = ('token', 'is_active', 'api')
    list_filter = ('is_active', 'api')
    search_fields = ('token',)