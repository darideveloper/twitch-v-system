from viwers import models as viwers_models
from core.tests import BaseTestApi

API_BASE = "viwers"
TOKEN = "token123*"

class TestBotsView (BaseTestApi): 
       
    # Setup test 
    api_base = API_BASE
    endpoint = "bots"
    token = TOKEN
    model = viwers_models.Bot
    auto_generate_data = True
    
    def test_invalid_token (self):
        self.base_invalid_token ()
        
    def test_invalid_token_delete (self):
        self.base_invalid_token ("delete")
        
    def test_invalid_token_delete (self):
        self.base_invalid_token ("put")
    
    def test_disable (self): 
        self.base_disable ()
        
    def test_disable_not_found (self):
        self.base_disable_not_found ()
 
    def test_get_no_registers (self): 
        self.base_get_no_registers ()
  
    def test_get (self):
        self.base_get ()
        
    def test_put (self):
        self.base_put ()

    def test_put_missing_fields (self):
        self.base_put_missing_fields ()