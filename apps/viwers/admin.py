from django.contrib import admin
from viwers import models

@admin.register(models.Bot)
class AdminBot (admin.ModelAdmin):
    list_display = ('user', 'is_active', 'last_update')
    list_filter = ('is_active', 'last_update')
    search_fields = ('user', 'password', 'cookies')
    readonly_fields = ('last_update',)