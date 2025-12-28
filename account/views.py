from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm

# Create your views here.

@login_required
def profile(request):
    form = UserProfileForm()
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            userprofile = form.save(commit=False)
            userprofile.user = request.user
            userprofile.save()
    return render(request, 'profile.html', {'form':form})
    

