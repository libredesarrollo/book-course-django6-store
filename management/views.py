from django.http import HttpResponse
from django.views.generic import FormView, View, TemplateView, UpdateView, CreateView, DeleteView, DetailView, ListView

from .forms import BookForm
from .models import Book

# Create your views here.
# **** CRUDs
class BookSaveFormView(FormView):
    template_name='book/save.html'
    form_class=BookForm
    success_url='/management/save/success'
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class BookUpdateView(UpdateView):
    model=Book
    template_name='book/save.html'
    form_class=BookForm
    success_url='/management/save/success'
    # fields=['name',]
    
class BookDeleteView(DeleteView):
    model=Book
    template_name='book/delete.html'
    success_url='/management/save/success'
    # fields=['name',]

class BookCreateView(CreateView):
    model=Book
    template_name='book/save.html'
    # form_class=BookForm
    success_url='/management/save/success'
    fields=['name', 'author']
    
class BookDetailView(DetailView):
    model=Book
    # por defecto el parametor es object o el nombre del modelo (book)
    # context_object_name='libro'
    template_name='book/detail.html'

class BookListView(ListView):
    model=Book
    # por defecto el parametor es object o el nombre del modelo (object_list)
    # context_object_name='books' # object_list
    template_name='book/index.html'



class BookSaveFormSuccessView(View):
    def get(self, request):
        return HttpResponse("El libro se creo, se feliz!")
    
class BookSaveFormSuccessTemplateView(TemplateView):
    template_name = 'book/success.html'