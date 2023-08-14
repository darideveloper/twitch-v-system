from core.views import BaseJsonGetView, BaseJsonGetDisableView, BaseJsonPostView
from comments import models

class Bots (BaseJsonGetDisableView):
    model = models.Bot     
    
class Comments (BaseJsonGetView):
    model = models.Comment
    
class Mods (BaseJsonGetView):
    model = models.Mod
    
class CommentsPhantom (BaseJsonGetView):
    model = models.Comment
    
class CommentsHistory (BaseJsonPostView):
    model = models.CommentHistory
    exclude_fields = ['datetime']
    foreign_fields = {
        "stream": models.Stream,
        "bot": models.Bot,
        "comment_mod": models.Comment,
        "mod": models.Mod 
    }