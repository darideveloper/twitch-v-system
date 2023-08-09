from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from apps.comments import urls as comments_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # redirect to admin page if access to the root
    path('', RedirectView.as_view(permanent=True, url='/admin/')),
    
    # add apps urls
    path('comments/', include(comments_urls)),
]