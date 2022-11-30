from django.db import models


class Usuario(models.Model):
    """
    Modelo Usuario

    Atributos:
        nombre (str): Representa la columna nombre en la base de datos. Máximo 35 caracteres
        primer_apellido (str): Representa la columna primer_apellido en la base de datos. Máximo 35 caracteres
        segundo_apellido (str): Representa la columna segundo_apellido en la base de datos. Máximo 35 caracteres.
        dni (str): Representa la columna dni en la base de datos. Máximo 9 caracteres
    """
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


class DocumentoFirmado(models.Model):
    """
    Modelo DocumentoFirmado

    Atributos:
        fecha (date): Representa la columna fecha en la base de datos.
        pdf(filefield): Representa la columna pdf en la base de datos y almacena un path al documento firmado.
        Usuario(fk): Representa la columna usuario y es una foreign key a la tabla Usuario
    """
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
