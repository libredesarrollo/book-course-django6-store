from django.core.exceptions import ValidationError

from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,blank=True)
    
    def __str__(self):
        return self.title
    
class Type(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,blank=True)
    
    def __str__(self):
        return self.title

class ElementManager(models.Manager):
    def get_queryset(self):
        # Siempre que usemos Element.objects.all(), incluirá el select_related
        return super().get_queryset().select_related('category', 'type')
    
class Element(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,blank=True)
    description = models.TextField() # blank=True, null=True
    price = models.DecimalField(max_digits=10,decimal_places=2, default=6.10) # 12345678.10
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #, related_name='elements'
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    
    # Asignamos el manager personalizado
    # objects = ElementManager()
    
    # Realizar validaciones desde el modelo y se aplican en los formularios
    # def clean(self):
    #     if self.price < 0:
    #         raise ValidationError('Price cannot be negative')
    
    def __str__(self):
        return self.title