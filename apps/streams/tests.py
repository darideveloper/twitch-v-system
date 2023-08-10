from streams import models as streams_models
from core.tests import BaseTestApi
from django.contrib.auth.models import User
from django.utils import timezone

API_BASE = "streams"
TOKEN = "token123*"

class TestStreams (BaseTestApi):
    
    def setUp (self): 
        
        now = timezone.now().astimezone(timezone.get_default_timezone())
        
        # Create users
        self.auth_user = User.objects.create_user (
            username="test_user",
            email="sample@gmail.com",
            password="test_password"       
        )
        self.auth_user.save ()
        
        
        self.streamer = streams_models.Streamer (
            auth_user=self.auth_user,
            twitch_user="test_twitch_user"
        )
        self.streamer.save ()
        
        # Create streams
        self.stream_now = streams_models.Stream (
            streamer=self.streamer,
            date=now, 
            start_time=now,
            end_time=now,
        ) 
        self.stream_now.save ()
        
        yesterday = now - timezone.timedelta(days=1)
        self.stream_outdated = streams_models.Stream (
            streamer=self.streamer,
            date=yesterday,
            start_time=yesterday,
            end_time=yesterday,            
        )
        self.stream_outdated.save ()
        
        self.models = [self.stream_now, self.stream_outdated]
        
        super().setUp()
    
    # Setup test
    api_base = API_BASE
    endpoint = "current-streams"
    token = TOKEN
    model = streams_models.Stream
    
    def test_invalid_token (self):
        self.base_invalid_token ()
        
    def test_disable (self): 
        self.base_disable ()
    
    def test_get_no_models (self): 
        self.base_get_no_models ()
    
    def test_get (self): 
         
        response = self.client.get(self.get_full_api())
        response_json = response.json()
        
        models = self.get_models()
        
        # Validate response generals
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response_json['status'], 'ok')
        self.assertEqual(response_json['message'], 'Data found')
        self.assertEqual(len(response_json['data']), len(models) - 1)
        
        # Validate response
        self.assertEqual(response_json['data'][0]['streamer'], self.stream_now.streamer.twitch_user)
        self.assertEqual(response_json['data'][0]['date'], self.stream_now.date.strftime("%Y-%m-%d"))
        self.assertEqual(response_json['data'][0]['start_time'][0:8], self.stream_now.start_time.strftime("%H:%M:%S"))
        self.assertEqual(response_json['data'][0]['end_time'][0:8], self.stream_now.end_time.strftime("%H:%M:%S"))