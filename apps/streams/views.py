from django.http import JsonResponse
from core.views import BaseDisableView
from streams import models
from core.decorators import validate_token
from django.utils import timezone

class CurrentStreams (BaseDisableView): 
    
    model = models.Stream
    
    @validate_token    
    def get (self, request): 
        
        # Get streams of the current hour
        now = timezone.now().astimezone(timezone.get_default_timezone())
        date = now.date()
        time = now.time()
        streams = self.get_data().filter (date=date, start_time__hour=time.hour)
        
        # Formmat data
        streams = list(streams.values())
        
        # add username 
        stramers = models.Streamer.objects.all()
        
        for stream in streams:
            streamer = stramers.get(id=stream['streamer_id'])
            stream['streamer'] = streamer.twitch_user
            stream['access_token'] = streamer.access_token
            
        # Remove unnecesary fields
        extra_fields = ['streamer_id']
        for stream in streams:
            for extra_field in extra_fields:
                del stream[extra_field]
        
        if streams:
            return JsonResponse({
                "status": 'ok',
                "message": 'Data found',
                "data": streams
            })
        else: 
            return JsonResponse({
                "status": 'error',
                "message": 'No data found',
                "data": []
            })