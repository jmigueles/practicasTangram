# IMPORTS DE DJANGO
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.conf import settings

# Importamos los modelos 
from .models import DocumentoFirmado, Usuario

# Imports de los formularios
from .forms import SolicitudForm 

# Librerías de python
from datetime import datetime
import base64

# Import funciones propias
from .functions import convert_to_pdf, date_format


def confirmacion_datos(request):    
    """
    Vista que muestra al usuario un formulario de solicitud y confirma tras el POST
    desde la plantilla que el formulario es válido, en caso contrario se le devuelve
    a la vista con los errores encontrados.
    """

    if request.method=='POST':
        form = SolicitudForm(request.POST)

        # Comprobación de que la validez del formulario
        if form.is_valid():
            try:
                usuario = Usuario.objects.get(dni=form.cleaned_data['dni'])
            except:
                usuario = Usuario.objects.create(
                    dni=form.cleaned_data['dni'],
                    nombre=form.cleaned_data['nombre'],
                    primer_apellido=form.cleaned_data['primer_apellido'],
                    segundo_apellido=form.cleaned_data['segundo_apellido']
                )
                usuario.save()
        
            return render(request, 'datos_formulario.html', {'usuario':usuario, 'texto':form.cleaned_data['texto'], 'fecha': datetime.today().strftime('%d-%m-%Y')})
        
        else:
            return render(request, 'formularios/formulario_solicitud.html', {'form': form, })

    # Renderizamos en función del control de validación
    return render(request, 'formularios/formulario_solicitud.html', {'form': SolicitudForm()})


def pdf_usuario_sin_firma(request):
    """
    Vista que renderiza la plantilla html 'pdf.html' junto con los datos introducidos
    por el usuario a pdf. Una vez hecho esto se mostrará al usuario.
    Si se intenta acceder por GET a la vista se retornará al usuario al inicio.
    """

    if request.method=='POST' and 'dni' in request.POST:
        # Contexto que pasaremos a la función para renderizar el pdf generado para el usuario
        try:
            usuario = Usuario.objects.get(dni=request.POST['dni'],)             
            fecha = datetime.strptime(request.POST['fecha'], '%d-%m-%Y')        
            contexto = {
                'nombre': usuario.nombre,
                'apellidos': usuario.primer_apellido + ' ' + usuario.segundo_apellido,
                'dni': usuario.dni,
                'texto': request.POST['texto'],
                'fecha': date_format(fecha)
            }

            # Se convierte el html en pdf
            filename = 'solicitud.pdf'
            template = 'pdf.html'
            conf = convert_to_pdf(template, filename, contexto)

            # Se comprueba si la conversión se llevo a cabo de forma adecuada
            if not conf: 
                return render(request, 'error.html', {'error': 'No pudimos generar el pdf con su solicitud, lo sentimos'})

            # Generado el pdf lo codificamos a base64
            with open(str(settings.PDF_GEN_DIR) + '/' + filename, 'rb') as pdf:
                stringBase64 = base64.b64encode(pdf.read())

            # Se renderiza el visor y se envía el contexto con los datos a mostrar
            return render(request, 'visor.html', {'pdf_base64': stringBase64,  'filename': filename, 'usuario': usuario, 'fecha': request.POST['fecha']})
        
        except:
            return render(request, 'error.html', {'error': 'No pudimos generar el pdf con su solicitud, lo sentimos'})
    
    # Si no se accede por POST será enviado al inicio
    return render(request, 'formularios/formulario_solicitud.html', {'form': SolicitudForm()})


def pdf_usuario_con_firma(request):
    """
    Vista que se encarga de guardar el documento firmado en la base de datos, más tarde
    en un directorio local junto con el dni de usuario y finalmente se retorna a la template 'visor.html'
    mostrándole el documento para descargar.
    """

    if request.method == 'POST' and 'firma' in request.POST:

        # Obtenemos el documento firmado y lo decodificamos
        b64 = request.POST['firma']
        bytes = base64.b64decode(b64,validate=True)

        try:
            # Guardamos el documento firmado en la base de datos
            usuario = Usuario.objects.get(dni=request.POST['dni'],)             
            fecha = datetime.strptime(request.POST['fecha'], '%d-%m-%Y')        
            doc_firm = DocumentoFirmado.objects.create(
                fecha = datetime.strftime(fecha, '%Y-%m-%d'),
                pdf = ContentFile(bytes, 'firma.pdf'),
                usuario = usuario,
            )
            # Registramos el documento
            doc_firm.save()

            # Guardamos el pdf en un directorio local del servidor
            filename = usuario.dni + 'doc_firmado.pdf'
            f = open(str(settings.PDF_FIRM_DIR) + '/' + filename, 'wb')
            f.write(bytes)
            f.close()

            # Renderizamos la vista del visor con el pdf firmado
            return render(request, 'visor.html', {'cert': doc_firm,})
        except:
            return render(request, 'error.html', {'error': 'No pudimos generar el pdf con su solicitud, lo sentimos'})
        
    # Si no se accede por POST será enviado al inicio
    return render(request, 'formularios/formulario_solicitud.html', {'form': SolicitudForm()}) 


    

