from django.db import models
from django.utils import timezone
from streams.models import Stream

def get_default_cookies ():
    return {"sample": "sample"}

class Bot (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100, verbose_name='Usuario de bot')
    password = models.CharField(max_length=100, verbose_name='Contraseña de bot')
    cookies = models.JSONField (default=get_default_cookies, verbose_name='Cookies de bot')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    class Meta:
        verbose_name = 'Bot'
        verbose_name_plural = 'Bots'
    
    def __str__(self):
        if self.is_active:
            return self.user
        else:
            return f"{self.user} (inactivo)"
 
class Comment (models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=200, verbose_name='Comentario de bot o mod')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Comentario de bots o mods'
        verbose_name_plural = 'Comentarios de bots y mods'
        
    def str (self):
        return self.comment
        
class Mod (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=200, verbose_name='Usuario de moderador')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Moderador'
        verbose_name_plural = 'Moderadores'
        
    def __str__(self):
        if self.is_active:
            return self.user
        else:
            return f"{self.user} (inactivo)"

class CommentPhantom (models.Model):
    id = models.AutoField(primary_key=True)
    comment_mod = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Comentario de un mod')
    comment_res = models.CharField(max_length=200, verbose_name='Comentario de respuesta')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Comentario fantasma'
        verbose_name_plural = 'Comentarios fantasma'
        
    def __str__(self):
        return f"{self.comment_mod} -> {self.comment_res}"
    
class CommentHistory (models.Model):
    id = models.AutoField(primary_key=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, verbose_name='Stream')
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, verbose_name='Bot')
    comment_phantom = models.ForeignKey(CommentPhantom, on_delete=models.CASCADE, verbose_name='Comentario fantasma')
    mod = models.ForeignKey(Mod, on_delete=models.CASCADE, verbose_name='Moderador', null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True, verbose_name='Fecha y hora')
    
    class Meta: 
        verbose_name = 'Historial de comentarios'
        verbose_name_plural = 'Historial de comentarios'
        
    def __str__(self):
        return f"{self.bot} - {self.comment_phantom__comment_res} - {self.datetime}"