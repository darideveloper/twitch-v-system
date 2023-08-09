from django.http import JsonResponse
from comments import models
from core.views import BaseJsonGetView, BaseJsonGetDisableView

class Bots (BaseJsonGetDisableView):
    model = models.Bot     
    
class Comments (BaseJsonGetView):
    model = models.Comment
    
class Mods (BaseJsonGetView):
    model = models.Mod
    
class CommentsPhantom (BaseJsonGetView):
    model = models.CommentPhantom
    
    def get (self, request):
        
        data = self.get_data()
        
        # Get only mods unique comments abd filter active
        mods_comments = list(set(map (lambda row: row.comment_mod, data)))
        mods_comments = list(filter(lambda row: row.is_active, mods_comments))
        
        # Get bots comments to each mod
        data_list = {}
        for comment_mod in mods_comments:
            
            # Get comments and filter only active comments
            bots_comments = data.filter (comment_mod=comment_mod)
            bots_comments = list(map (lambda row: row.comment_res, bots_comments))
            bots_comments = list(filter(lambda row: row.is_active, bots_comments))
            
            # Get only comments text
            bots_comments = list(map (lambda row: row.comment, bots_comments))
            
            data_list[comment_mod.comment] = bots_comments
            
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