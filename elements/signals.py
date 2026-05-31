from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import PermissionDenied

@receiver(pre_save)
def block_saves(sender, instance, **kwargs):
    model_name = sender.__name__
    
    # 1. Allow writing session information
    if model_name in ('Session', 'SessionStore'):
        return
        
    # 2. Allow existing User updates (e.g., updating last_login on login)
    if model_name == 'User' and instance.pk is not None:
        return

    raise PermissionDenied("¡Modo Demo Activo! No se permiten crear o modificar registros en la base de datos.")

@receiver(pre_delete)
def block_deletes(sender, instance, **kwargs):
    model_name = sender.__name__
    
    # Allow session cleanup
    if model_name in ('Session', 'SessionStore'):
        return
        
    raise PermissionDenied("¡Modo Demo Activo! No se permiten eliminar registros de la base de datos.")
