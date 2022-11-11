# Imports de django
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.conf import settings

# Librerías de terceros 
from xhtml2pdf import pisa

# Librerías de python
import re
import os 

'''
    validarDNI(dni):
        Recibe como argumento el dni del usuario. 
        Comprobará su validez primeramente ejecutando una expresión regular y posteriormente
        comprobará si es válido lógicamente.
'''
def validarDNI(dni):
    # Letras para comprobar la validez del caracter
    letras = 'TRWAGMYFPDXBNJZSQVHLCKET'
    # Control de validez del dni 
    valido = False

    # Validaciones
    if re.match("^[XYZ]?\d{7,8}[A-Z]$", dni):
        numero = dni[0:len(dni)-1]
        numero = numero.replace('X', '0')
        numero = numero.replace('Y', '1')
        numero = numero.replace('Z', '2')

        # Comprobamos si cumple la lógica
        valido = letras[int(numero)%23] == dni[len(dni)-1]    

    return valido

'''
    validar(nombre, apellidos, dni, texto)
        Recibe como argumentos los datos introducidos por el usuario en la solicitud
        y aplica una comprobación sencilla de su validez
'''
def validar(nombre, apellidos, dni, texto):
    # RegExp
    regExpNomApe = "^[\sa-zA-ZñÑá-úÁ-Úä-ÿÄËÏÖÜ]{2,35}$" 
    ok = False

    # Validamos
    if re.match(regExpNomApe, nombre) and re.match(regExpNomApe, apellidos) and validarDNI(dni) and (len(texto) > 0 and len(texto) <= 512):
        ok = True
    
    return ok

def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path
'''
    convert_to_pdf(template, context={})
        Convierte una template pasada como argumento junto con el contexto dado a pdf.
'''
def convert_to_pdf(template, context={}):
    # Creamos el archivo que contendrá el pdf temporalmente
    archivo = open(str(settings.PDF_DIR) + '/' + 'reporte.pdf', 'wb+')
    # Renderizamos la template con el contexto
    template = get_template(template)
    html = template.render(context)
    # Creamos el pdf y lo guardamos en el destino indicado anteriormente
    status = pisa.CreatePDF(html, dest=archivo, link_callback=link_callback)

    # Comprobamos si existen errores
    if status.err:
        return False

    return True
'''

def convert_to_pdf(template, context={}):
    # Recogemos y renderizamos la template
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    
    file = open('static/pdfs_firmados/reporte.pdf', 'wb+')
    template = get_template(template)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=file, link_callback=link_callback)

    print(pisa_status)
    # Creamos un buffer en memoria para mostrarla al usuario y aplicamos codificación
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    # Comprobamos la existencia de errores
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return None
'''
    
        