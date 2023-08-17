from core.views import BaseGetView, BaseDisableView, BasePostView
from comments import models

class Bots (BaseGetView, BaseDisableView):
    model = models.Bot     
    
class Comments (BaseGetView):
    model = models.Comment
    
class Mods (BaseGetView):
    model = models.Mod
    
class CommentsPhantom (BaseGetView):
    model = models.Comment
    
class CommentsHistory (BasePostView):
    model = models.CommentHistory
    exclude_fields = ['datetime']
    foreign_fields = {
        "stream": models.Stream,
        "bot": models.Bot,
        "comment_mod": models.Comment,
        "mod": models.Mod 
    }