from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def get_next_hour (): 
    # Deprecated
    return None

def get_now ():
    now = timezone.now().astimezone(timezone.get_default_timezone())
    return now

class Streamer (models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario de autenticación')
    twitch_user = models.CharField(max_length=50, verbose_name='Usuario de Twitch')
    
    def __str__ (self):
        return self.twitch_user
        
class Stream (models.Model):
    id = models.AutoField(primary_key=True)
    streamer = models.ForeignKey(Streamer, on_delete=models.CASCADE, verbose_name='Usuario de Twitch')
    date = models.DateField(verbose_name='Fecha', default=get_now)
    start_time = models.TimeField(verbose_name='Hora de inicio', default=get_now)
    end_time = models.TimeField(verbose_name='Hora de fin', default=get_now)
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    class Meta:
        verbose_name = 'Stream'
        verbose_name_plural = 'Streams'
        
    def __str__ (self):
        return f"{self.streamer} - {self.date} - {self.start_time}"