from django.contrib import admin

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    save_as = True
    save_as_continue = False
    save_on_top = True
    list_display = ('id', 'text') #, 'upper_title'
    list_editable = ('text',)
    search_fields = ('text', 'id')
    date_hierarchy = 'date_posted'
    list_filter = ('date_posted',)
    fields = ('text', )

    # @admin.display(description="Title")
    # def upper_title(self, obj):
    #     return f"{obj.id} - {obj.text}".upper()

    def save_model(self, request, obj, form, change):
        """
        Se ejecuta al guardar un objeto (ya sea al crearlo o al actualizarlo).
        'change' es True si se está actualizando un objeto existente.
        'change' es False si se está creando un nuevo objeto.
        """
        if change:
            print(f"--- Guardando cambios en el comentario ID: {obj.pk} ---")
        else:
            print(f"--- Creando un nuevo comentario ---")
        
        # Llamamos al método original para que el objeto se guarde correctamente
        super().save_model(request, obj, form, change)
        print(f"--- El comentario ID: {obj.pk} ha sido guardado en la base de datos. ---")

    def delete_model(self, request, obj):
        """
        Se ejecuta al eliminar un único objeto desde su página de edición.
        """
        print(f"--- Eliminando el comentario ID: {obj.pk} ---")
        
        # Llamamos al método original para que el objeto se elimine correctamente
        super().delete_model(request, obj)
        print(f"--- El comentario ID: {obj.pk} ha sido eliminado. ---")

    def delete_queryset(self, request, queryset):
        """
        Se ejecuta al usar la acción "Eliminar comentarios seleccionados" en la lista.
        'queryset' es un conjunto de los objetos que se van a eliminar.
        """
        count = queryset.count()
        print(f"--- Eliminando un queryset de {count} comentarios ---")
        
        # Llamamos al método original para que los objetos se eliminen correctamente
        super().delete_queryset(request, queryset)
        print(f"--- Los {count} comentarios han sido eliminados. ---")

    def save_formset(self, request, form, formset, change):
        """
        Se ejecuta al guardar formularios en línea (inlines) asociados al objeto principal.
        """
        print(f"--- Guardando un formset (inlines) para el comentario principal ---")
        super().save_formset(request, form, formset, change)
        print(f"--- El formset ha sido guardado. ---")


# Register your models here.
#admin.site.register(Comment, CommentAdmin)
