from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
# from django.contrib.auth.models import User

# Create your views here.

class UserLoginView(LoginView):
    template_name='user/login.html'
    redirect_authenticated_user = True
    next_page='/management'
    extra_context = {
        'key1': 'Key 1'
    }
    
class UserLogoutView(LogoutView):
    # template_name='user/logout.html'
    next_page='/login'
    
class UserRegisterCreateView(CreateView):
    template_name='user/register.html'
    form_class=UserCreationForm
    success_url='/login'
    
    