from django.urls import path

from . import views


urlpatterns = [
    path("crip", views.crip, name="crip"),
    path("cifrados", views.cifrados, name="cifrados"),
    path("hash_python", views.hash_python, name="hash_python"),
    path("hash_django", views.hash_django, name="hash_django"),
    path("my_session", views.my_session, name="my_session"),
]
