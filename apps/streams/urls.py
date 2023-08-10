from django.urls import path
from streams import views

urlpatterns = [
    path ('current-streams/', views.CurrentStreams.as_view(), name='current-streams'),
]