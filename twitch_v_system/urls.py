from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    # redirect to admin page if access to the root
    path('', RedirectView.as_view(permanent=True, url='/admin/')),
    path('admin/', admin.site.urls),
]
