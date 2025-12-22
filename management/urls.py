from django.urls import path

from .views import BookSaveFormView

app_name = 'comments'
urlpatterns = [
    path("save", BookSaveFormView.as_view()),
]
