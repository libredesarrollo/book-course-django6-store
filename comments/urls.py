from django.urls import path

from .views import add
from . import views

app_name = 'comments'
urlpatterns = [
    path("add", add, name="add"),
    path('', views.index, name='index'),
    path('update/<int:pk>', views.update, name='update'),
    path('delete/<int:pk>', views.delete, name='delete'),
]
