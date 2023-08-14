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

class BaseJsonGetView (View):
    """ Get data from model and return as json
    """
    
    model = None
    
    def get_data (self):
        return self.model.objects.all()
    
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
class BaseJsonGetDisableView (BaseJsonGetView):
    """ Get data from model, return as json 
        and disable register from model
    """
    
    @validate_token
    def delete (self, request):
                
        # Get id from json
        data = json.loads(request.body)
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
class BaseJsonPostView (View):
    """ Get data from madal, return as json
        and create new register
    """
    
    exclude_fields = []
    foreign_fields = {}
    
    def get_exclude_fields (self):
        return self.exclude_fields
    
    @validate_token
    def post (self, request):
        
        exclude_fields = self.get_exclude_fields()
        fields = get_model_fields(self.model, related_fields=True)
                
        # Get data from json
        data = json.loads(request.body)
        
        # Validate all fields in data
        data_formated = {}
        for field in fields:
            
            if field.name in exclude_fields:
                continue
            
            # Validate if fields exist
            if field.name not in data:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Field {field.name} is required',
                    'data': []
                }, status=400)
                
            # Validate foreign fields
            if field.name in self.foreign_fields.keys():
                
                related_register = self.foreign_fields[field.name].objects.filter(id=data[field.name])
                                
                if related_register.exists():
                    data[field.name] = related_register.first()
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Field {field.name} is not valid',
                        'data': []
                    }, status=400)
    
        # Create new register
        register = self.model(**data)
        register.save()
        
        # Return response
        return JsonResponse({
            'status': 'ok',
            'message': 'Register disabled',
            'data': {
                "id": register.id
            },
        })