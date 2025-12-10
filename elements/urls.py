from django.urls import path

from .views import add, index, update, delete

app_name = 'elements'
urlpatterns = [
    path('', index, name='index'),
    path("add", add, name="add"),
    path('update/<int:pk>', update, name='update'),
    path('delete/<int:pk>', delete, name='delete'),
]
