from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail

from .models import Comment

@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, created, **kwargs):
    pass
    # send_mail(
    #     subject="Prueba HTML",
    #     message="Este es el mensaje de respaldo", # Texto plano
    #     from_email="noreply@tusitio.com",
    #     recipient_list=["usuario@ejemplo.com"],
    #     html_message="<h1>¡Hola Mundo!</h1>", # Contenido con etiquetas
    # )
    # print('Comment Created!')