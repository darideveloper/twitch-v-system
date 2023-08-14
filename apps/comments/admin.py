from django.contrib import admin
from comments import models

@admin.register(models.Bot)
class AdminBot (admin.ModelAdmin):
    list_display = ('user', 'is_active', 'last_update')
    list_filter = ('is_active', 'last_update')
    search_fields = ('user', 'password', 'cookies')
    readonly_fields = ('last_update',)

@admin.register(models.Comment)
class AdminComments (admin.ModelAdmin):
    list_display = ('category', 'comments', 'is_active', 'last_update')
    list_filter = ('category', 'is_active', 'last_update')
    search_fields = ('category', 'comment',)
    readonly_fields = ('last_update',)
    
@admin.register(models.Mod)
class AdminMods (admin.ModelAdmin):
    list_display = ('user', 'is_active', 'last_update')
    list_filter = ('is_active', 'last_update')
    search_fields = ('user',)
    readonly_fields = ('last_update',)

@admin.register(models.CommentHistory)
class AdminCommentsHistory (admin.ModelAdmin):
    list_display = ('stream', 'bot', 'comment_mod', 'comment_bot', 'datetime')
    list_filter = (
        'stream__streamer', 
        'comment_mod__category', 
        'bot__user',
        'datetime', 
        'mod__user'
    )
    search_fields = (
        'stream__streamer',
        'comment_mod__category',
        'comment_bot',
        'bot__user',
        'mod__user'
    )
    readonly_fields = ('datetime',)
    raw_id_fields = ('stream', 'comment_mod')