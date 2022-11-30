from django.contrib import admin
from .models import DocumentoFirmado, Usuario

''' ---------------------------------------------------
        PERSONALIZACIÓN DEL MODEL DEL DOCUMENTO
--------------------------------------------------- '''
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'pdf')
    search_fields = ('fecha',)

admin.site.register(DocumentoFirmado, DocumentoAdmin)

''' ---------------------------------------------------
        PERSONALIZACIÓN DEL MODEL DEL USUARIO
--------------------------------------------------- '''
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'primer_apellido', 'segundo_apellido', 'dni')
    search_fields = ('primer_apellido', 'dni')

admin.site.register(Usuario, UsuarioAdmin)