from django.urls import path

from . import views


urlpatterns = [
    path("crip", views.crip, name="crip")
]
