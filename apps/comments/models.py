from django.db import models
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
    category = models.CharField(max_length=200, verbose_name='Comentario del mod')
    comments = models.TextField(verbose_name='Comentarios posibles de bot (uno por línea)')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        
    def __str__ (self):
        comments_num = len(self.comments.split('\n'))
        return f"{self.category} ({comments_num} bot comments)"
        
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
    
class CommentHistory (models.Model):
    id = models.AutoField(primary_key=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, verbose_name='Stream')
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, verbose_name='Bot')
    comment_mod = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Comentario')
    comment_bot = models.CharField(max_length=200, verbose_name='Comentario de bot')
    mod = models.ForeignKey(Mod, on_delete=models.CASCADE, verbose_name='Moderador', null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True, verbose_name='Fecha y hora')
    
    class Meta: 
        verbose_name = 'Historial de comentarios'
        verbose_name_plural = 'Historial de comentarios'
        
    def __str__(self):
        return f"{self.bot} - {self.comment_mod} - {self.datetime}"