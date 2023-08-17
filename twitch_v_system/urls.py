from django.contrib import admin
from django.urls import path, include
from apps.comments import urls as comments_urls
from apps.streams import urls as streams_urls
from apps.viwers import urls as viwers_urls
from apps.core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # redirect to admin page if access to the root
    path('', core_views.redirect_admin, name='redirect_admin'),
    
    # add apps urls
    path('comments/', include(comments_urls)),
    path('streams/', include(streams_urls)), 
    path('viwers/', include(viwers_urls)), 
]