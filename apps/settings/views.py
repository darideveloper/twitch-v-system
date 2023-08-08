from django.shortcuts import render, redirect
from django.views.generic import RedirectView

class RedirectAdmin (RedirectView):
    
    permanent = False
    
    def get_redirect_url(self, *args, **kwargs):
        return redirect('/admin/')