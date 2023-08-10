from django.contrib import admin
from streams import models

@admin.register(models.Streamer)
class StreamerAdmin (admin.ModelAdmin):
    list_display = ('auth_user', 'twitch_user')
    search_fields = ('auth_user', 'twitch_user', 'auth_user__is_active')

@admin.register(models.Stream)
class StreamAdmin (admin.ModelAdmin):
    list_display = ('streamer', 'date', 'start_time', 'end_time', 'is_active')
    list_filter = ('streamer', 'date', 'start_time', 'end_time', 'is_active')