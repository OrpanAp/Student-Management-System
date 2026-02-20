from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import views as auth_views

class HomeView(generic.TemplateView):
    template_name = "base/home.html"
    
class FeatureView(generic.TemplateView):
    template_name = "base/feature.html"
    
class UserLoginView(auth_views.LoginView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        # If user is already authenticated, redirect to home
        if request.user.is_authenticated:
            return redirect('home')  # or your preferred page
        return super().dispatch(request, *args, **kwargs)
    

