from comments import models as comments_models
from core.tests import BaseTestApi

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
    
    def test_disable (self): 
        self.base_disable ()
 
    def test_get_no_models (self): 
        self.base_get_no_models ()
  
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

    def test_get_no_models (self): 
        self.base_get_no_models ()
        
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
        
    def test_get_no_models (self): 
        self.base_get_no_models ()
    
    def test_get (self):
        self.base_get ()
        
class TestCommentsPhamtomView (BaseTestApi): 
        
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
    model = comments_models.CommentPhantom
    
    def test_invalid_token (self):
        self.base_invalid_token ()
    
    def test_get_no_models (self): 
        self.base_get_no_models ()
    
    def test_get (self):
        
        response = self.client.get(self.get_full_api())
        response_json = response.json()
        
        models = self.get_models()
        
        # Validated response generals
        self.assertEqual(response.status_code, 200)
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
    