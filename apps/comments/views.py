from core.views import BaseJsonGetView, BaseJsonGetDisableView
from comments import models

class Bots (BaseJsonGetDisableView):
    model = models.Bot     
    
class Comments (BaseJsonGetView):
    model = models.Comment
    
class Mods (BaseJsonGetView):
    model = models.Mod
    
class CommentsPhantom (BaseJsonGetView):
    model = models.Comment