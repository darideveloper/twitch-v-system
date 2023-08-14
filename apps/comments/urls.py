from django.urls import path
from comments import views

urlpatterns = [
    path ('bots/', views.Bots.as_view(), name='bots'),
    path ('comments/', views.Comments.as_view(), name='comments'),
    path ('mods/', views.Mods.as_view(), name='mods'),
]

