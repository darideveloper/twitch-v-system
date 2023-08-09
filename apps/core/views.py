import json
from django.views import View
from django.http import JsonResponse
from core.decorators import validate_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class BaseJsonGetView (View):
    """ Get data from model and return as json
    """
    
    model = None
    
    def get_data (self):
        return self.model.objects.all()
    
    @validate_token
    def get (self, request):
        
        print ("get method")
        
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
    """ Get data from model and return as json 
        and disable register from model
    """
    
    @validate_token
    def delete (self, request):
        
        # query item
        item = self.get_data().filter(id=1)
        if not item.exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Register not found',
                'data': []
            }, status=400)
            
        # disable register
        item = item.first()
        item.is_active = False
        item.save()
        
        return JsonResponse({
            'status': 'ok',
            'message': 'Register disabled',
            'data': []
        })
        
        