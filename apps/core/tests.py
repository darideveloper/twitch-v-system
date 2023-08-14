import json
from django.test import TestCase
from core import models as code_models
from core.tools import get_model_fields

class BaseTestApi (TestCase): 
    
    api_base = ""
    endpoint = ""
    models = []
    token = ""
    model = None
    auto_generate_data = False
    
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
    
    def get_model (self):
        return self.model
    
    def get_auto_generate_data (self):
        return self.auto_generate_data
    
    def setUp (self):
        """ Setup headers and auto generate data """
        
        # Create models with random data
        model = self.get_model()
        auto_generate_data = self.get_auto_generate_data()
        if auto_generate_data:
            
            fields = get_model_fields(model)
            
            auto_data = {}
            fields_types = {
                "CharField": "test",
                "BooleanField": True,
                "IntegerField": 1,
                "FloatField": 1.0,
                "DateTimeField": "2020-01-01 00:00:00",
                "DateField": "2020-01-01",
                "TimeField": "00:00:00",
                "TextField": "test",
                "ForeignKey": 1,
                "ManyToManyField": 1,
                "OneToOneField": 1,
                "EmailField": "sample@gmail.com",
                "URLField": "https://www.google.com",
                "UUIDField": "123e4567-e89b-12d3-a456-426614174000",
                "GenericIPAddressField": "192.168.1.254",
                "JSONField": json.dumps({"test": "test"}),
            }
            for field in fields:
                
                # Get field data type
                field_type = field.get_internal_type()
                field_data = fields_types.get (field_type, None)
                
                if not field_data:
                    raise Exception (f"Field type '{field_type}' not found, and auto_generate_data is True") 
                
                # Save field sample data
                auto_data[field.name] = field_data
                
            # Create model instances with auto data
            model_1 = model(**auto_data)
            model_1.save()
            model_2 = model(**auto_data)
            model_2.save()
            self.models = [model_1, model_2]
        
        # Create token and headers
        token = code_models.Token (
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
        
        # Get models and columns
        models = self.get_models()
        model = self.get_model()
        fields = get_model_fields(model)
        
        # Validated response generals
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'ok')
        self.assertEqual(response_json['message'], 'Data found')        
        self.assertEqual(len(response_json["data"]), len(models))
        
        # Validate response data (each field in each row of models)
        rows_counter = 0
        for row in response_json["data"]:
            for field in fields: 
                       
                self.assertEqual(row[field.name], getattr(models[rows_counter], field.name))
                
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
        
        model = self.get_model()
        model_id = 1
        
        response = self.client.delete(
            self.get_full_api(),
            json.dumps({"id": model_id}),
            content_type="application/json"
        )
        
        with open ("temp.html", "w") as file: 
            file.write (str(response.content))
        
        response_json = response.json()
        
        # Validate response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'ok')
        self.assertEqual(response_json['message'], 'Register disabled')
        
        self.assertEqual(len(response_json["data"]), 0)
        
        # Validate models
        model1 = model.objects.get(id=model_id)
        self.assertFalse(model1.is_active)
        
        