import json
from django.test import TestCase
from settings import models as settings_models
from comments import models

class BaseTestApiGet (TestCase): 
    
    api_base = None
    endpoint = None
    models = None
    token = None
    
    def get_api_base (self): 
        return self.api_base
    
    def get_endpoint (self): 
        return self.endpoint
    
    def get_models (self): 
        return self.models
    
    def get_token (self):
        return self.token

    def get_full_api (self): 
        return f"/{self.get_api_base()}/{self.get_endpoint()}/"
    
    def setUp (self):
        
        # Create token and headers
        token = settings_models.Token (
            api=self.get_api_base(),
            token=self.get_token()
        )
        token.save()
        self.client.defaults["HTTP_token"] = self.get_token()
        
    
    def base_invalid_token (self):
        """ Test invalid token """
                
        # Change token 
        self.client.defaults["HTTP_token"] = "invalid token"
        
        response = self.client.get(self.get_full_api())
        response_json = response.json()
        
        # Validated response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['status'], 'error')
        self.assertEqual(response_json['message'], 'Invalid token')
    
    def base_get (self):
                        
        response = self.client.get(self.get_full_api())
        response_json = response.json()
        
        # Get models columns
        models = self.get_models()
        fields = models[0].__dict__.keys()
        
        # Remove extra fields
        skip_fields = ["_state", "id", "last_update", "created"]
        fields = list (filter (lambda field: field not in skip_fields, fields))
        
        # Validated response generals
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'ok')
        self.assertEqual(response_json['message'], 'Data found')        
        self.assertEqual(len(response_json["data"]), len(models))
        
        # Validate response data (each field in each row of models)
        rows_counter = 0
        for row in response_json["data"]:
            for field in fields: 
                       
                self.assertEqual(row[field], getattr(models[rows_counter], field))
                
            rows_counter += 1
            
    def base_get_no_models (self):
        """ Test query model without register """
        
        # Delete models
        models = self.get_models()
        for model in models:
            model.delete()
        
        response = self.client.get(self.get_full_api())
        response_json = response.json()
        
        # Validate response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'error')
        self.assertEqual(response_json['message'], 'No data found')
        
        self.assertEqual(len(response_json["data"]), 0)       
    
    def base_disable (self): 
        """ Test disable register """
        
        model_id = 1
        
        response = self.client.delete(
            self.get_full_api(),
            json.dumps({"id": model_id}),
            content_type="application/json"
        )
        response_json = response.json()
        
        # Validate response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'ok')
        self.assertEqual(response_json['message'], 'Register disabled')
        
        self.assertEqual(len(response_json["data"]), 0)
        
        # Validate models
        bot1 = models.Bot.objects.get(id=model_id)
        self.assertFalse(bot1.is_active)
        
        