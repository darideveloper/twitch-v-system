import requests

# Add parent folder to path
import os
import sys
from dotenv import load_dotenv
parent_folder = os.path.dirname(os.path.dirname(__file__))
apps_folder = os.path.join(parent_folder, "apps")
sys.path.append(parent_folder)
sys.path.append(apps_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitch_v_system.settings')
django.setup()
from django.utils import timezone
from streams import models as streams_models

load_dotenv()

TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET")

# Get current datetime od the time zone
now = timezone.now()

# Get users
users = streams_models.Streamer.objects.filter()
for user in users:
    
    if not user.refresh_token:
        print (f"User {user} has no refresh token")
        continue
    
    # Get new token
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "refresh_token": user.refresh_token,
        "grant_type": "refresh_token"
    }
    res = requests.post(url, data=params)
    res.raise_for_status ()

    json_data = res.json()
    access_token = json_data.get("access_token", "")
    if not access_token:
        raise Exception (f"No access token in json: {json_data}")

    # Update user token
    user.access_token = access_token
    user.save()
    print (f"Updated token for user {user}")