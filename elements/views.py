from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .forms import ElementForm # ,ElemementModelForm
from .models import Element, Category, Type

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
    
    # categoria ejemplo
    # categorias = Category.objects.prefetch_related('elements').all()
    # for cat in categorias:
    #     print(f"Categoría: {cat.title}")
    #     # Aquí Django hace una consulta a la DB por CADA categoría para buscar sus elementos
    #     for el in cat.element_set.all(): 
    #         print(f" - Elemento: {el.title}")
    # categoria ejemplo
    
    elements = Element.objects.all()
    # elements = Element.objects.select_related('category', 'type').all()
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

def blog_list(request):
    elements = Element.objects.all().order_by('-created')
    
    # Filters
    type_slug = request.GET.get('type')
    category_slug = request.GET.get('category')

    if type_slug:
        elements = elements.filter(type__slug=type_slug)
    
    if category_slug:
        elements = elements.filter(category__slug=category_slug)

    # Pagination
    paginator = Paginator(elements, 6) # 6 elements per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    types = Type.objects.all()
    categories = Category.objects.all()

    return render(request, 'elements/blog_list.html', {
        'page_obj': page_obj,
        'types': types,
        'categories': categories,
        'selected_type': type_slug,
        'selected_category': category_slug
    })

def blog_detail(request, slug):
    element = get_object_or_404(Element, slug=slug)
    return render(request, 'elements/blog_detail.html', {'element': element})