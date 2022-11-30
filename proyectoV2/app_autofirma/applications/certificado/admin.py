from django.contrib import admin
from .models import DocumentoFirmado, Usuario


class DocumentoAdmin(admin.ModelAdmin):
    """
    DocumentoAdmin. Se modifica el administrador del DocumentoFirmado 
    para mostrar las columnas añadiendo además un buscado por fecha
    """
    list_display = ('usuario', 'fecha', 'pdf')
    search_fields = ('fecha',)

admin.site.register(DocumentoFirmado, DocumentoAdmin)


class UsuarioAdmin(admin.ModelAdmin):
    """
    UsuarioAdmin. Se modifica el administrador del modelo Usuario para
    mostrar las columnas añadiendo un campo de búsqueda por primer apellido
    o dni
    """
    list_display = ('nombre', 'primer_apellido', 'segundo_apellido', 'dni')
    search_fields = ('primer_apellido', 'dni')

admin.site.register(Usuario, UsuarioAdmin)