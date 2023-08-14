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