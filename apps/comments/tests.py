import json
from django.test import TestCase
from comments import models as comments_models
from settings import models as settings_models
from core.tests import BaseTestApiGet

API_BASE = "comments"
TOKEN = "token123*"

class TestBotsView (BaseTestApiGet): 
        
    def setUp (self): 
        
        # Create models
        bot1 = comments_models.Bot (
            user="bot1user",
            password="bot1pass",
            cookies={"bot1cookie": "bot1cookie"},
        )
        bot1.save()
        
        bot2 = comments_models.Bot (
            user="bot2user",
            password="bot2pass",
            cookies={"bot2cookie": "bot2cookie"},
            is_active=False
        )
        bot2.save()
        
        self.models = [bot1, bot2]
        
        super().setUp()
   
    # Setup test 
    api_base = API_BASE
    endpoint = "bots"
    token = TOKEN
    
    def test_invalid_token (self):
        self.base_invalid_token ()
        
    def test_get (self):
        self.base_get ()
    
    def test_get_no_models (self): 
        self.base_get_no_models ()
    
    def test_disable (self): 
        self.base_disable ()
        
class TestCommentsView (BaseTestApiGet): 
        
    def setUp (self): 
        
        # Create models
        comment1 = comments_models.Comment (
            comment="hello1", 
        )
        comment1.save()
        
        comment2 = comments_models.Comment (
            comment="hello2", 
            is_active=False
        )
        comment2.save()
        
        self.models = [comment1, comment2]
        
        super().setUp()
   
    # Setup test 
    api_base = API_BASE
    endpoint = "comments"
    token = TOKEN
    
    def test_invalid_token (self):
        self.base_invalid_token ()
        
    def test_get (self):
        self.base_get ()
    
    def test_get_no_models (self): 
        self.base_get_no_models ()
        
class TestModsView (BaseTestApiGet): 
        
    def setUp (self): 
        
        # Create models
        mod1 = comments_models.Mod (
            user="mod2", 
        )
        mod1.save()
        
        mod2 = comments_models.Mod (
            user="mod2", 
            is_active=False
        )
        mod2.save()
        
        self.models = [mod1, mod2]
        
        super().setUp()
   
    # Setup test 
    api_base = API_BASE
    endpoint = "mods"
    token = TOKEN
    
    def test_invalid_token (self):
        self.base_invalid_token ()
        
    def test_get (self):
        self.base_get ()
    
    def test_get_no_models (self): 
        self.base_get_no_models ()
        
class TestCommentsPhamtomView (BaseTestApiGet): 
        
    def setUp (self): 
        
        # Create models
        self.comment_a = comments_models.Comment (
            comment="hello", 
        )
        self.comment_a.save()
        
        self.comment_b = comments_models.Comment (
            comment="world",
        )
        self.comment_b.save()
        
        comment_phantom_1 = comments_models.CommentPhantom (
            comment_mod=self.comment_a,
            comment_res=self.comment_b,
        )
        comment_phantom_1.save()
        
        comment_phantom_2 = comments_models.CommentPhantom (
            comment_mod=self.comment_b,
            comment_res=self.comment_a,
        )
        comment_phantom_2.save()
        
        self.models = [comment_phantom_1, comment_phantom_2]
        
        super().setUp()
   
    # Setup test 
    api_base = API_BASE
    endpoint = "comments-phantom"
    token = TOKEN
    
    def test_invalid_token (self):
        self.base_invalid_token ()
    
    def test_get (self):
        
        response = self.client.get(self.get_full_api())
        response_json = response.json()
        
        models = self.get_models()
        
        # Validated response generals
        self.assertEqual(response_json['status'], 'ok')
        self.assertEqual(response_json['message'], 'Data found')        
        self.assertEqual(len(response_json["data"]), len(models))
        
        # Validate response data
        self.assertEqual(response_json["data"][self.comment_a.comment], [
            self.comment_b.comment,
        ])
        
        self.assertEqual(response_json["data"][self.comment_b.comment], [
            self.comment_a.comment,
        ])
    
    def test_get_no_models (self): 
        self.base_get_no_models ()