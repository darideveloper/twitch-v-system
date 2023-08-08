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
    list_display = ('comment', 'is_active', 'last_update')
    list_filter = ('is_active', 'last_update')
    search_fields = ('comment',)
    readonly_fields = ('last_update',)
    
@admin.register(models.Mod)
class AdminMods (admin.ModelAdmin):
    list_display = ('user', 'is_active', 'last_update')
    list_filter = ('is_active', 'last_update')
    search_fields = ('user',)
    readonly_fields = ('last_update',)
    
@admin.register(models.CommentPhantom)
class AdminCommentsPhantom (admin.ModelAdmin):
    list_display = ('comment_mod', 'comment_res', 'last_update')
    list_filter = ('comment_mod', 'last_update',)
    search_fields = ('comment_mod', 'comment_res')
    readonly_fields = ('last_update',)

@admin.register(models.CommentHistory)
class AdminCommentsHistory (admin.ModelAdmin):
    list_display = ('stream', 'bot', 'comment_phantom', 'datetime')
    list_filter = (
        'stream__streamer', 
        'comment_phantom__comment_mod', 
        'bot__user',
        'datetime', 
        'mod__user'
    )
    search_fields = (
        'stream__streamer',
        'comment_phantom__comment_mod',
        'comment_phantom__comment_res',
        'bot__user',
        'mod__user'
    )
    readonly_fields = ('datetime',)
    raw_id_fields = ('stream', 'comment_phantom')