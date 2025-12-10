from django import forms

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils.text import slugify

from .models import Element, Type, Category

class ElementForm(forms.Form):
    # title = forms.CharField(label="Título", max_length=255, min_length=3, validators=[MinLengthValidator(5, message='Very short! (min %(limit_value)d) current %(show_value)d ')])
    title = forms.CharField(label="Título", max_length=255, min_length=3, 
                            validators=[
                                MinLengthValidator(5,)
                                ])
    description = forms.CharField(label='Descripción', initial='Tu increible post por aquí', widget=forms.Textarea, validators=[MinLengthValidator(2, message='Very short! (min %(limit_value)d) current %(show_value)d ')])

    slug = forms.SlugField(label='Slug', max_length=255, widget=forms.TextInput(
        attrs = {
            'id': '50',
            'class': 'form-control'
        }
    ))
    # description = forms.CharField(widget=forms.Textarea, initial='Content Initial')
    price = forms.DecimalField(label='Price', decimal_places=2, max_digits=5, required=False)

    type = forms.ModelChoiceField(queryset=Type.objects.all(), initial=1)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=1)

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if Element.objects.filter(title=title).exists():
    #         raise ValidationError("Title already exists")
    #     return title
    
    # def clean(self):
    #     form_data = self.cleaned_data
    #     if form_data["slug"] != slugify(form_data["title"]):
    #         self._errors["slug"] = ["Slug do not match with title"]
    #     return form_data


class ElemementModelForm(forms.ModelForm):
    class Meta:
        model = Element
        fields = '__all__'

