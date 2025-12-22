from django.shortcuts import render
from django.views.generic import FormView

from .forms import BookForm

# Create your views here.

class BookSaveFormView(FormView):
    template_name='book/save.html'
    form_class=BookForm
    success_url='book/management/save/success'
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    