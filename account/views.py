import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm
from .models import UserProfile

# Create your views here.

@login_required
def profile(request):

    # Intentamos obtener el perfil existente, si no existe, será None
    try:
        userprofile = request.user.userprofile
    except UserProfile.DoesNotExist:
        userprofile = None

    if request.method == "POST":
        
        # Guardamos la ruta del avatar viejo ANTES de actualizar el modelo
        # Usamos una referencia al archivo físico actual
        old_avatar_path = None
        if userprofile.avatar:
            old_avatar_path = userprofile.avatar.path
        
        # Pasamos la instancia (si existe) para que Django sepa que es UPDATE y no INSERT
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
                
        if form.is_valid():
            # 1. Manejo del borrado del avatar viejo (opcional)
            if 'avatar' in request.FILES and old_avatar_path:
                if os.path.exists(old_avatar_path):
                    os.remove(old_avatar_path)

            # 2. Guardar el perfil
            profile_instance = form.save(commit=False)
            profile_instance.user = request.user  # Aseguramos el usuario
            profile_instance.save()
            
            return redirect('profile') # Es buena práctica redirigir tras un POST exitoso
    else:
        form = UserProfileForm(instance=userprofile)

    return render(request, 'profile.html', {'form': form})
    

