from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .forms import ElementForm # ,ElemementModelForm
from .models import Element

# Create your views here.

def add(request):
    if request.method == "POST":
        form = ElementForm(request.POST)
        if form.is_valid():
            element = Element()
            element.title = form.cleaned_data['title']
            element.slug = form.cleaned_data['slug']
            element.description = form.cleaned_data['description']
            element.price = form.cleaned_data['price']
            element.type = form.cleaned_data['type']
            element.category = form.cleaned_data['category']
            element.save()
    else:
        form = ElementForm()

    return render(request, 'elements/add.html', {'form':form})

def index(request):
    elements = Element.objects.all()
    paginator = Paginator(elements, 15)
    page_number = request.GET.get('page')
    elements_page = paginator.get_page(page_number)
    return render(request,'elements/index.html',{'elements':elements_page})


def update(request, pk):
    
    element = get_object_or_404(Element, pk=pk)

    if request.method == "POST":
        form = ElementForm(request.POST)
        if form.is_valid():
            element.title = form.cleaned_data['title']
            element.slug = form.cleaned_data['slug']
            element.description = form.cleaned_data['description']
            element.price = form.cleaned_data['price']
            element.type = form.cleaned_data['type']
            element.category = form.cleaned_data['category']
            element.save()
    else:
         form = ElementForm(initial={
            'title': element.title, 
            'slug': element.slug, 
            'description': element.description,
            'price': element.price, 
            'type': element.type, 
            'category': element.category
        })

    return render(request,'elements/add.html',{'form':form, 'element': element})
    
def delete(request,pk):
    element = Element.objects.get(pk=pk)
    element.delete()
    return redirect('elements:index')