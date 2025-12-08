from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Element, Category, Type

class ElementInline(admin.TabularInline):
    model = Element
    extra = 1

@admin.register(Type, Category)
class CategoryTypeAdmin(admin.ModelAdmin):
    # list_display = ('id','title')
    # class Media:
    #     css = {
    #         "all": ["my_styles.css"],
    #     }
    #     js = ["my_code.js"]
    
    def save_model(self, request, obj, form, change):
        if obj.slug == '':
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)

    # inlines = [
    #     ElementInline,
    # ]
    
    

# **** Para manejar el formulario aparte y tener opciones de personalizar el mismo
# class ElementForm(forms.ModelForm):
#     class Meta:
#         model = Element
#         exclude = ["title"]    
        
#     def clean_price(self):
#         if self.cleaned_data.get('price') < 0:
#             raise ValidationError('Price cannot be negative')
	
@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    # **** SOLO si quieres personalizar el campo
    # form=ElementForm

    def save_model(self, request, obj, form, change):
        if obj.slug == '':
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)

    # **** Personalizar los campos por divisiones - Mas completo
    # fieldsets = [
    #     (
    #         "Regular options",
    #         {
    #             "fields": ["slug", "title", "description"],
    #         },
    #     ),
    #     (
    #         "Advanced options",
    #         {
    #             "fields": ["price",],
    #         },
    #     ),
    # ]
    
    list_display = ('id','title','category','type')
    
    # # fields = ('title','slug','description','price','category','type', )
    # **** Personalizar los campos por divisiones - Mas simple
    fields = (('title','slug'),'description','price',('category','type', ))