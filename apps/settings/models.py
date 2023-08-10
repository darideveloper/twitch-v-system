from django.db import models

class Token (models.Model):
    
    apis = [
        ('comments', 'Comentarios'),
        ('streams', 'Streams'),
        ('viwers', 'Viwers'),
    ]
    
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=100, verbose_name='Token de Twitch')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    api = models.CharField(max_length=100, choices=apis, verbose_name='API')
    
    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        
    def __str__ (self):
        return self.token