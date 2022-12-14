from django.db import models


''' ------------------------------------------------------------------------
    MODELO USUARIO:
        Se recogerán los datos de los usuarios
------------------------------------------------------------------------ '''
class Usuario(models.Model):
    # Campos de la tabla
    nombre = models.CharField(max_length=35)
    primer_apellido = models.CharField(max_length=35)
    segundo_apellido = models.CharField(max_length=35)
    dni = models.CharField(max_length=9, unique=True)

    # Meta
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    # Métodos
    def __str__(self):
        return self.nombre + ' ' + self.primer_apellido

''' ------------------------------------------------------------------------
    MODELO CERTIFICADO:
        Se recogerán los pdf firmados de los usuarios junto con sus datos
------------------------------------------------------------------------ '''
class DocumentoFirmado(models.Model):
    # Campos de la tabla
    fecha = models.DateField()
    pdf = models.FileField(null=True, upload_to='solicitudes_firmadas')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='modelo')

    # Meta
    class Meta:
        verbose_name = 'Documento firmado'
        verbose_name_plural = 'Documentos firmados'
        

    # Métodos
    def __str__(self):
        return str(self.fecha)
