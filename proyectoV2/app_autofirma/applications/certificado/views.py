# IMPORTS DE DJANGO
from django.shortcuts import render
from django.utils.html import strip_tags
from django.core.files.base import ContentFile
from django.conf import settings

# Librerías de python
from datetime import datetime
import base64

# Import funciones propias
from .functions import validar, convert_to_pdf, date_format

# Importamos los modelos 
from .models import Documento_firmado, Usuario


''' -----------------------------------------------------------
                    Vista para el formulario
------------------------------------------------------------'''
def formulario_solicitud(request):
    return render(request, 'formularios/formulario_solicitud.html')


''' -----------------------------------------------------------
                    Vista para validar los datos
------------------------------------------------------------'''
def confirmacion_datos(request):
    # Control de validación
    ok = False
    
    # Comprobamos que lleguen los datos requeridos
    if 'nombre_usuario' in request.POST and 'dni_usuario' in request.POST and 'texto_usuario' in request.POST and 'apellido1_usuario' in request.POST and 'apellido2_usuario' in request.POST:

        # Los limpiamos de espacios y posibles etiquetas html
        nombre = str.strip(strip_tags(request.POST['nombre_usuario']))
        apellido1 = str.strip(strip_tags(request.POST['apellido1_usuario']))
        apellido2 = str.strip(strip_tags(request.POST['apellido2_usuario']))
        dni = str.strip(strip_tags(request.POST['dni_usuario']))
        texto = str.strip(strip_tags(request.POST['texto_usuario']))

        # Validamos
        if validar(nombre, apellido1, apellido2, dni, texto):
            # Extraemos el usuario de la BD, si no existe lo creamos
            try:
                usuario = Usuario.objects.get(dni=dni)
            except:
                usuario = Usuario(
                        dni = dni,
                        nombre = nombre,
                        primer_apellido = apellido1,
                        segundo_apellido = apellido2,
                    )
                # Registramos al usuario en la BD
                usuario.save()         

            # Controlamos la validacióin
            ok = True

    # Renderizamos en función del control de validación
    if ok:
        return render(request, 'datos_formulario.html', {'usuario': usuario, 'texto':texto, 'fecha': datetime.today().strftime('%d-%m-%Y') })
    else:
        return render(request, 'formularios/formulario_solicitud.html', {'error': 'Los datos enviados no son válidos'})


''' -----------------------------------------------------------
                    Vista para renderizar los pdf
------------------------------------------------------------'''
def pdf_usuario(request):
    
    # Si recibimos el documento firmado por el usuario
    if 'firma' in request.POST:

        # Obtenemos el documento firmado y lo decodificamos
        b64 = request.POST['firma']
        bytes = base64.b64decode(b64,validate=True)

        # Guardamos el documento firmado en la base de datos
        usuario = Usuario.objects.get(dni=request.POST['dni'],)             # Obtenemos el usuario para registrarlo en el documento firmado
        fecha = datetime.strptime(request.POST['fecha'], '%d-%m-%Y')        # Formateo de fecha para la BD
        doc_firm = Documento_firmado.objects.create(
            fecha = datetime.strftime(fecha, '%Y-%m-%d'),
            pdf = ContentFile(bytes, 'firma.pdf'),
            usuario = usuario,
        )
        # Registramos el documento
        doc_firm.save()

        # Guardamos el pdf para mostrarlo al usuario
        filename = 'doc_firmado.pdf'
        f = open(str(settings.PDF_FIRM_DIR) + '/' + filename, 'wb')
        f.write(bytes)
        f.close()

        # Renderizamos la vista del visor con el pdf firmado
        return render(request, 'visor.html', {'filename': filename, 'cert': doc_firm})

    # Si recibimos el dni del usuario renderizamos el documento pdf a firmar
    elif 'dni' in request.POST:

        # Contexto que pasaremos a la función para renderizar el pdf generado para el usuario
        usuario = Usuario.objects.get(dni=request.POST['dni'],)             # Obtenemos el usuario para rellenar la plantilla de pdf junto con el texto
        fecha = datetime.strptime(request.POST['fecha'], '%d-%m-%Y')        # Formateamos la fecha para que sea más amigable para el usuario
        contexto = {
            'nombre': usuario.nombre,
            'apellidos': usuario.primer_apellido + ' ' + usuario.segundo_apellido,
            'dni': usuario.dni,
            'texto': request.POST['texto'],
            'fecha': date_format(fecha)
        }

        # Convertimos el html en pdf
        filename = 'solicitud.pdf'
        conf = convert_to_pdf('pdf.html', filename, contexto)

        # Comprobamos si la conversión se llevo a cabo de forma adecuada
        if not conf:
            return render(request, 'error.html', {'error': 'No pudimos generar el pdf con su solicitud, lo sentimos'})

        # Generado el pdf lo codificamos a base64
        with open(str(settings.PDF_GEN_DIR) + '/' + filename, 'rb') as pdf:
            stringBase64 = base64.b64encode(pdf.read())

        # Generamos la respuesta para el usuario
        return render(request, 'visor.html', {'pdf_base64': stringBase64,  'filename': filename, 'usuario': usuario, 'fecha': request.POST['fecha']})

    # Si no recibimos los campos esperados renderizamos una vista de error
    return render(request, 'error.html', {'error': 'No se han recibido los datos esperados, lo sentimos'})


    

