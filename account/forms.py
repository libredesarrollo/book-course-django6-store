from django.core.files.images import get_image_dimensions

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar','user','address', 'language', 'age')
        widgets = {
            'user': forms.HiddenInput(),
            'address': forms.Textarea(attrs={'rows':3})
        }
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            # Validar extensión
            extension = avatar.name.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png']:
                raise forms.ValidationError("Solo se permiten archivos JPG o PNG.")
            
            # Validar dimensiones (opcional)
            width, height = get_image_dimensions(avatar)

            if width < 200 or height < 200:
                raise forms.ValidationError("La imagen debe ser de al menos 200x200 píxeles.")
            if width > 1024 or height > 1024:
                raise forms.ValidationError("La imagen es muy grande y debe ser menor a 1024x1024 píxeles.")
            return avatar
