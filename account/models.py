from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    class Language(models.IntegerChoices):
        ES = 0
        En = 1
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.ImageField(upload_to='user/avatar')
    
    address = models.CharField(max_length=200, default='')
    language = models.IntegerField(default=Language.ES, choices=Language)
    age = models.PositiveIntegerField(default=0)
