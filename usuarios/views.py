from django.shortcuts import render
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm

class CustomLoginView(auth_views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

