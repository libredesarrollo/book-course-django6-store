from django.urls import path

from .views import BookSaveFormView, BookSaveFormSuccessView, BookSaveFormSuccessTemplateView, BookUpdateView, BookCreateView, BookDeleteView, BookDetailView, BookListView

urlpatterns = [
    # CRUD
    path("", BookListView.as_view()),
    path("index", BookListView.as_view()),
    path("save", BookSaveFormView.as_view()),
    path("create", BookCreateView.as_view()),
    path("detail/<int:pk>", BookDetailView.as_view()),
    path("update/<int:pk>", BookUpdateView.as_view()),
    path("delete/<int:pk>", BookDeleteView.as_view()),
    # path("save/success", BookSaveFormSuccessView.as_view()),
    path("save/success", BookSaveFormSuccessTemplateView.as_view()),

    
]
