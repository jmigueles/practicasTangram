# IMPORTS DE DJANGO
from django.shortcuts import render
from django.utils.html import strip_tags
from django.views.generic import TemplateView

# IMPORTS funciones propias
from .functions import validar, convert_to_pdf

# Librerías de python
from datetime import date


# Vista que muestra el formulario de solicitud
class Formulario_solicitud(TemplateView):
    template_name = 'formularios/formulario_solicitud.html'


# Vista que valida los datos
def confirmacion_datos(request):
    # Control de validación
    ok = False
    
    # Comprobamos que lleguen los datos requeridos
    if 'nombre_usuario' in request.POST and 'dni_usuario' in request.POST and 'texto_usuario' in request.POST:

        # Los limpiamos de espacios y posibles etiquetas html
        nombre = str.strip(strip_tags(request.POST['nombre_usuario']))
        apellidos = str.strip(strip_tags(request.POST['apellidos_usuario']))
        dni = str.strip(strip_tags(request.POST['dni_usuario']))
        texto = str.strip(strip_tags(request.POST['texto_usuario']))

        # Validamos
        if validar(nombre,apellidos, dni, texto): ok = True

    # Renderizamos en función del control de validación
    if ok:
        return render(request, 'datos_formulario.html', {'nombre':nombre, 'apellidos': apellidos, 'dni':dni, 'texto':texto, 'fecha': date.today() })
    else:
        return render(request, 'formularios/formulario_solicitud.html', {'error': 'Datos manipulados en el cliente'})

# Vista que genera un pdf válido para el usuario
def pdf_usuario(request):
    # Contexto que pasaremos a la función para renderizar el pdf
    contexto = {
        'nombre': request.POST['nombre'],
        'apellidos': request.POST['apellidos'],
        'dni': request.POST['dni'],
        'texto': request.POST['texto'],
        'fecha': request.POST['fecha']
    }

    # COnvertimos el html en pdf
    pdf = convert_to_pdf('pdf.html', contexto)

    # Generamos la respuesta para el usuario
    return render(request, 'visor.html')





    

