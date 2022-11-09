from django.db import models

''' ------------------------------------------------------------------------
    MODELO CERTIFICADO:
        Se recogerán los pdf firmados de los usuarios junto con sus datos
------------------------------------------------------------------------ '''
class Certificado(models.Model):
    # Campos de la tabla
    nombre = models.CharField(max_length=35)
    apellidos = models.CharField(max_length=35)
    dni = models.CharField(max_length=9)
    fecha = models.DateField()
    texto = models.CharField(max_length=512)
    pdf_firmado = models.BinaryField()

    # Meta
    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'

    # Métodos
    def __str__(self):
        return self.nombre + ' ' + self.apellidos + ' ' + ' ' + self.dni

    