import json
from django.views import View
from django.http import JsonResponse
from core.decorators import validate_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from core.tools import get_model_fields

def redirect_admin (request):
    # Redirect to admin page
    return redirect('/admin/') 

# def redirect_login (request):
#     # Redirect update-token
#     return redirect('/streams/update-token/')

class Base (View):
    """ Bese template for endpoints
    """

    model = None
    exclude_fields = []
    foreign_fields = {}
    
    def get_model (self):
        return self.model
        
    def get_data (self):
        return self.model.objects.all()
    
    def get_exclude_fields (self):
        return self.exclude_fields
    
    def get_foreign_fields (self):
        return self.foreign_fields
    
    def __get_comming_data__ (self, body:object, fields:list) -> dict:
        """ Validate if fields exists in json data

        Args:
            body (object): request body with json data
            fields (list): list of fields to validate

        Returns:
            dict: 
                status (str): status of the json validation
                message (str): message of the json validation
                data (dict): data from json
        """
        
        # Try to load json
        try:
            data = json.loads(body)
        except:
            return {
                'status': 'error',
                'message': 'Invalid json',
                'data': []
            }
        
        exclude_fields = self.get_exclude_fields()
        foreign_fields = self.get_foreign_fields()
        
         # Validate all fields in data
        for field in fields:
            
            if field.name in exclude_fields:
                continue
            
            # Validate if fields exist
            if field.name not in data:
                return {
                    'status': 'error',
                    'message': f'Field {field.name} is required',
                    'data': []
                }
                
            # Validate foreign fields
            if field.name in foreign_fields.keys():
                
                related_register = foreign_fields[field.name].objects.filter(id=data[field.name])
                                
                if related_register.exists():
                    data[field.name] = related_register.first()
                else:
                    return {
                        'status': 'error',
                        'message': f'Field {field.name} is not valid',
                        'data': []
                    }
        
        return data
    
class BaseGetView (Base):
    """ Get data from model and return as json
    """
    
    @validate_token
    def get (self, request):
                
        # Return wuqryset as json
        data = self.get_data()
        data_list = list(data.values())
        
        if not data_list:
            return JsonResponse({
                'status': 'error',
                'message': 'No data found',
                'data': []
            })
        
        return JsonResponse({
            'status': 'ok',
            'message': 'Data found',
            'data': data_list
        })
        
@method_decorator(csrf_exempt, name='dispatch')
class BaseDisableView (Base):
    """ Disable register from model
    """
    
    @validate_token
    def delete (self, request):
        
        # Try to load json
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid json',
                'data': []
            }, status=400)
         
        # Get id from json
        json_id = data.get('id', None)
        
        register = self.get_data().filter(id=json_id)
        if not register.exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Register not found',
                'data': []
            }, status=400)
            
        # disable register
        register = register.first()
        register.is_active = False
        register.save()
        
        return JsonResponse({
            'status': 'ok',
            'message': 'Register disabled',
            'data': []
        })

@method_decorator(csrf_exempt, name='dispatch')
class BasePostView (Base):
    """ Create new register
    """
    
    @validate_token
    def post (self, request):
        
        model = self.get_model()
        fields = get_model_fields(model, related_fields=True)
        
        # Validate json contents
        data_formatted = self.__get_comming_data__(request.body, fields)
        if "status" in data_formatted and data_formatted["status"] == "error":
            return JsonResponse(data_formatted, status=400)
    
        # Create new register
        register = model(**data_formatted)
        register.save()
        
        # Return response
        return JsonResponse({
            'status': 'ok',
            'message': 'Register created',
            'data': {
                "id": register.id
            },
        })
        
@method_decorator(csrf_exempt, name='dispatch')
class BasePutView (Base):
    """ Create new register
    """
    
    @validate_token
    def put (self, request):
        
        model = self.get_model()
        fields = get_model_fields(model, related_fields=True, get_id=True)
        
        # Validate json contents
        data_formatted = self.__get_comming_data__(request.body, fields)
        if "status" in data_formatted and data_formatted["status"] == "error":
            return JsonResponse(data_formatted, status=400)
    
        # Create new register
        register = model.objects.filter(id=data_formatted["id"])
        if not register.exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Register not found',
                'data': []
            }, status=400)
            
        register = register.first()
        for key, value in data_formatted.items():
            setattr(register, key, value)
        register.save()
        
        # Return response
        return JsonResponse({
            'status': 'ok',
            'message': 'Register updated',
            'data': []
        })