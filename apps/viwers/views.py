from core.views import BaseGetView, BasePutView, BaseDisableView
from viwers import models

class Bots (BaseGetView, BasePutView, BaseDisableView):
    model = models.Bot