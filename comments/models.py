from django.db import models

from elements.models import Element


# Create your models here.

class Comment(models.Model):
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    # element = models.ForeignKey('elements.Element', on_delete=models.SET_NULL, null=True)
    element = models.ForeignKey(Element, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Comment {self.text} for {self.element.title if self.element else 'N/A'} - {self.date_posted.strftime('%Y-%m-%d')}"




