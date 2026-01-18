from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from unfold.admin import ModelAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Element, Category, Type

class ElementInline(admin.TabularInline):
    model = Element
    extra = 1

@admin.register(Type, Category)
class CategoryTypeAdmin(ModelAdmin):
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

class ElementResource(resources.ModelResource):
    class Meta:
        model = Element

@admin.register(Element)
class ElementAdmin(ModelAdmin, ImportExportModelAdmin):
    # **** SOLO si quieres personalizar el campo
    # form=ElementForm
    resource_class = ElementResource

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