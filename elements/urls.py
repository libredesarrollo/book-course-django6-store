from django.urls import path

from .views import add, index, update, delete, blog_list, blog_detail

app_name = 'elements'
urlpatterns = [
    path('', index, name='index'),
    path("add", add, name="add"),
    path('update/<int:pk>', update, name='update'),
    path('delete/<int:pk>', delete, name='delete'),
    path('blog/', blog_list, name='blog_list'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
]
