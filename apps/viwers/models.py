from django.db import models

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