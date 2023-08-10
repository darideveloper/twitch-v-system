from django.urls import path
from viwers import views

urlpatterns = [
    path ('bots/', views.Bots.as_view(), name='bots'),
]