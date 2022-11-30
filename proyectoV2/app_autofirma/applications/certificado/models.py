from django.db import models


# Modelo Usuario
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

# Modelo Certificado
class DocumentoFirmado(models.Model):
    # Campos de la tabla
    fecha = models.DateField()
    pdf = models.FileField(null=True, upload_to='solicitudes_firmadas')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='modelo')

    # Meta
    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        
    # Métodos
    def __str__(self):
        return str(self.fecha)
