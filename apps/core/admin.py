from django.contrib import admin
from django.contrib import admin
from core import models

admin.site.site_header = "Twitch V System"
admin.site.site_title = 'Twitch V System'
admin.site.site_url = '/'
admin.site.index_title = "Admin"

@admin.register(models.Token)
class TokenAdmin (admin.ModelAdmin):
    list_display = ('token', 'is_active', 'api')
    list_filter = ('is_active', 'api')
    search_fields = ('token',)