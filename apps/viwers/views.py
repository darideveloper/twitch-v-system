from core.views import BaseJsonGetDisableView
from viwers import models

class Bots (BaseJsonGetDisableView):
    model = models.Bot     