from django.contrib.auth.models import User
from comments import models as comments_models
from streams import models as streams_models
from core.tests import BaseTestApi
from django.utils import timezone

API_BASE = "comments"
TOKEN = "token123*"

class TestBotsView (BaseTestApi): 
       
    # Setup test 
    api_base = API_BASE
    endpoint = "bots"
    token = TOKEN
    model = comments_models.Bot
    auto_generate_data = True
    
    def test_invalid_token (self):
        self.base_invalid_token ()
        
    def test_invalid_token_delete (self):
        self.base_invalid_token ("delete")
    
    def test_disable (self): 
        self.base_disable ()
    
    def test_disable_not_found (self):
        self.base_disable_not_found ()
 
    def test_get_no_registers (self): 
        self.base_get_no_registers ()
  
    def test_get (self):
        self.base_get ()
    
        
class TestCommentsView (BaseTestApi): 
       
    # Setup test 
    api_base = API_BASE
    endpoint = "comments"
    token = TOKEN
    model = comments_models.Comment
    auto_generate_data = True
    
    def test_invalid_token (self):
        self.base_invalid_token ()

    def test_get_no_registers (self): 
        self.base_get_no_registers ()
        
    def test_get (self):
        self.base_get ()
    
class TestModsView (BaseTestApi): 

    # Setup test 
    api_base = API_BASE
    endpoint = "mods"
    token = TOKEN
    model = comments_models.Mod
    auto_generate_data = True
    
    def test_invalid_token (self):
        self.base_invalid_token ()
        
    def test_get_no_registers (self): 
        self.base_get_no_registers ()
    
    def test_get (self):
        self.base_get ()
        
class TestCommentsHistoryView (BaseTestApi):
    
    # Setup test
    api_base = API_BASE
    endpoint = "comments-history"
    token = TOKEN
    model = comments_models.CommentHistory
    auto_generate_data = False
    
    def setUp (self):
        
        now = timezone.now().astimezone(timezone.get_default_timezone())
        
        # Create users
        self.auth_user = User.objects.create_user (
            username="test_user",
            email="sample@gmail.com",
            password="test_password"       
        )
        self.auth_user.save ()
        
        # Create streamer
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
        
        # Create mod
        self.mod = comments_models.Mod (
            user="sample_mod",
        )
        self.mod.save ()
        
        # Create bot
        self.bot = comments_models.Bot (
            user="sample_bot",
            password="sample_password",
            cookies={"sample": "sample"}
        )
        self.bot.save ()
        
        # Crete comment
        self.comment = comments_models.Comment (
            category="sample_category",
            comments="sample_comment1\nsample_comment2\nsample_comment3",
        )
        self.comment.save()
        
        self.related_models = {
            "stream": streams_models.Stream,
            "bot": comments_models.Bot,
            "comment_mod": comments_models.Comment,
            "mod": comments_models.Mod,
        }
        
        super().setUp()
    
    def test_invalid_token (self):
        self.base_invalid_token ("post")
    
    def test_post (self):
        self.base_post ()
    
    def test_post_missing_fields (self):
        self.base_post_missing_fields ()
    