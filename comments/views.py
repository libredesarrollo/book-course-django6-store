from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator

from .models import Comment
from .forms import CommentForm


# Create your views here.

# **** samacuca!!! no usar
# def add(request):
#     if request.method == 'GET':
#         return render(request, 'comments/add.html')
#     else:
#         comment = Comment()
#         comment.text = request.POST.get('text')
#         comment.save()
#         return HttpResponse(request.POST.get('text'))
#     # return HttpResponse("Hello world!")
#     # return "HTTP"
def add(request):
    if request.method == 'GET':
        form = CommentForm()
        return render(request, 'comments/add.html', {'form':form})
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
        
        return redirect('comments:index')
        # return HttpResponse("Hello world!")
    # return "HTTP"

# sin paginar
# def index(request):
#     comments = Comment.objects.all()
#     return render(request,'comments/index.html',{'comments':comments})

def index(request):
    comments = Comment.objects.all()
    paginator = Paginator(comments, 15)
    page_number = request.GET.get('page')
    comments_page = paginator.get_page(page_number)
    return render(request,'comments/index.html',{'comments':comments_page})


def update(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
    else:
        form = CommentForm(instance=comment)

    # return render(request,'comments/add.html',{'form':form, 'comment': comment})
    return redirect('comments:index')


def delete(request,pk):
    # comment = Comment.objects.get(pk=pk)
    # comment.delete()
    return redirect('comments:index')
    # return HttpResponse("OK!")
