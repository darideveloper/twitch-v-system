import json
from django.db import models
from django.test import TestCase
from core import models as code_models
from core.tools import get_model_fields

class BaseTestApi (TestCase): 
    
    api_base = ""
    endpoint = ""
    registers = []
    token = ""
    model = None
    auto_generate_data = False
    related_models = []
    
    def __get_api_base__ (self): 
        return self.api_base
    
    def __get_endpoint__ (self): 
        return self.endpoint
    
    def __get_registers__ (self): 
        return self.registers
    
    def __get_token__ (self):
        return self.token

    def __get_full_api__ (self): 
        return f"/{self.__get_api_base__()}/{self.__get_endpoint__()}/"
    
    def __get_model__ (self):
        return self.model
    
    def __get_auto_generate_data__ (self):
        return self.auto_generate_data
    
    def __get_related_models__ (self):
        return self.related_models
    
    def setUp (self):
        """ Setup headers and auto generate data """
        
        # Create registers with random data
        model = self.__get_model__()
        auto_generate_data = self.__get_auto_generate_data__()
        
        self.fields_types = {
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
                
        if auto_generate_data:
            
            # Get model fields
            fields = get_model_fields(model)
    
            auto_data = {}
            
            for field in fields:
                    
                # Get field data type
                field_type = field.get_internal_type()
                field_data = self.fields_types.get (field_type, None)
                
                if not field_data:
                    raise Exception (f"Field type '{field_type}' not found, and auto_generate_data is True") 
                
                # Save field sample data
                auto_data[field.name] = field_data
                
            # Create model instances with auto data
            register_1 = model(**auto_data)
            register_1.save()
            register_2 = model(**auto_data)
            register_2.save()
            self.registers = [register_1, register_2]
        
        # Create token and headers
        token = code_models.Token (
            api=self.__get_api_base__(),
            token=self.__get_token__()
        )
        token.save()
        self.client.defaults["HTTP_token"] = self.__get_token__()
        
    
    def base_invalid_token (self, method:str="get"):
        """ Test invalid token

        Args:
            method (str, optional): HTTP method (get, post, put, delete). Defaults to "get".
        """
                
        # Change token 
        self.client.defaults["HTTP_token"] = "invalid token"
        
        if method == "get":
            response = self.client.get(self.__get_full_api__())
        elif method == "post":
            response = self.client.post(self.__get_full_api__())
        elif method == "put":
            response = self.client.put(self.__get_full_api__())
        elif method == "delete":
            response = self.client.delete(self.__get_full_api__())
        else:
            raise Exception (f"Method '{method}' not found")
            
        response_json = response.json()
        
        # Validated response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['status'], 'error')
        self.assertEqual(response_json['message'], 'Invalid token')
    
    def base_get (self):
        """ Test query model """
                        
        response = self.client.get(self.__get_full_api__())
        response_json = response.json()
        
        # Get registers and columns
        registers = self.__get_registers__()
        model = self.__get_model__()
        fields = get_model_fields(model)
        
        # Validated response generals
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'ok')
        self.assertEqual(response_json['message'], 'Data found')        
        self.assertEqual(len(response_json["data"]), len(registers))
        
        # Validate response data (each field in each row of registers)
        rows_counter = 0
        for row in response_json["data"]:
            for field in fields: 
                       
                self.assertEqual(row[field.name], getattr(registers[rows_counter], field.name))
                
            rows_counter += 1
            
    def base_get_no_registers (self):
        """ Test query model without register """
        
        # Delete registers
        registers = self.__get_registers__()
        for model in registers:
            model.delete()
        
        response = self.client.get(self.__get_full_api__())
        response_json = response.json()
        
        # Validate response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'error')
        self.assertEqual(response_json['message'], 'No data found')
        
        self.assertEqual(len(response_json["data"]), 0)       
    
    def base_disable (self): 
        """ Test disable register """
        
        model = self.__get_model__()
        model_id = self.__get_registers__()[0].id
        
        response = self.client.delete(
            self.__get_full_api__(),
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
        
        # Validate registers
        register_1 = model.objects.get(id=model_id)
        self.assertFalse(register_1.is_active)
        
    def base_post (self): 
        """ Test add new register to model """
        
        related_models = self.__get_related_models__()
        
        # Get model fields 
        model = self.__get_model__()
        fields_regular = get_model_fields(model)
        fields_all =  get_model_fields(model, related_fields=True)
        fields_related = list(set(fields_all) - set(fields_regular))
        
        # Generate sample data for related fields
        json_data = {}
        for field in fields_regular:
            
            # Get field data type
            field_type = field.get_internal_type()
            field_data = self.fields_types.get (field_type, None)
            
            if not field_data:
                raise Exception (f"Field type '{field_type}' not found, and auto_generate_data is True") 
            
            # Save field sample data
            json_data[field.name] = field_data
            
        # Generale sample data for related fields
        for field in fields_related:
            
            related_model =  related_models[field.name]
            related_registers = related_model.objects.all()
            
            # Validate related registers
            if len(related_registers) == 0:
                raise Exception (f"Related registers for '{field.name}' not found")
            
            # Save related register id
            json_data[field.name] = related_registers[0].id
            
        response = self.client.post(
            self.__get_full_api__(),
            json.dumps(json_data),
            content_type="application/json"
        )
        response_json = response.json()
        
        # Get and validate register created
        register_created = model.objects.filter(id=response_json["data"]["id"])
        if not register_created:
            raise Exception ("Register not created")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'ok')
        self.assertEqual(response_json['message'], 'Register created')
        self.assertEqual(response_json['data'], {"id": register_created[0].id})