from django.urls import path

from .views import UserLoginView, UserLogoutView, UserRegisterCreateView

urlpatterns = [
    path("login", UserLoginView.as_view()),
    path("logout", UserLogoutView.as_view(), name='logout'),
    path("register", UserRegisterCreateView.as_view(), name='register'),
]
