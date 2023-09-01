import os
import json
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from django.shortcuts import redirect
import requests
from dotenv import load_dotenv
from streams import models
from core.views import BaseDisableView
from core.decorators import validate_token

load_dotenv()
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
HOST = os.getenv("HOST")

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
            
class UpdateToken (View): 
    
    def get (self, request): 
        
        error = False
        
        current_path = f"{HOST}/streams/update-token/"

        # Try to get login code from twitch, after login
        login_code = request.GET.get("code", "")
        print (login_code)

        # Detect error in login
        if login_code:
            
            # Get twitch tokens
            token_url = "https://id.twitch.tv/oauth2/token"
            params = {
                "client_id": TWITCH_CLIENT_ID,
                "client_secret": TWITCH_CLIENT_SECRET,
                "code": login_code,
                "grant_type": "authorization_code",
                "redirect_uri": current_path,
            }
            try:
                res = requests.post(token_url, data=params)
                res.raise_for_status()
                json_data = json.loads(res.content)

                # Extract variables
                access_token = json_data.get("access_token", "")
                refresh_token = json_data.get("refresh_token", "")
            except Exception as error:
                return JsonResponse({
                    "status": "error",
                    "message": f"Error getting token: {error}",
                    "data": []
                })
                
            # Get user info
            user = request.user
            streamer = models.Streamer.objects.get(auth_user=user)
            streamer.access_token = access_token
            streamer.refresh_token = refresh_token
            streamer.save()          

        else:
            # Redirect to login twitch page
            twitch_scope = [
                "openid",
                "user:read:email",
                "chat:read",
                "moderator:read:chatters",
            ]
            url_params = {
                "client_id": TWITCH_CLIENT_ID,
                "redirect_uri": current_path,
                "response_type": "code",
                "force_verify": "false",
                "scope": " ".join(twitch_scope),
                "state": "sample_string",
                "claims": '{"userinfo":{"picture":null, "email":null, "name":null, "user": null, "preferred_username": null}}'
            }
            encoded_params = "&".join(
                [f"{param_key}={param_value}" for param_key, param_value in url_params.items()])
            twitch_link = f"https://id.twitch.tv/oauth2/authorize?{encoded_params}"
            
            return redirect(twitch_link)

        return redirect('/')
