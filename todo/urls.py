from django.urls import path

from .views import index

urlpatterns = [
    # CRUD
    path("", index),    
]