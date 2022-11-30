# Imports de django
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.conf import settings

# Librerías de terceros 
from xhtml2pdf import pisa

# Librerías de python
import os 


def link_callback(uri, rel):
    """
    Convierte las URIs del settings para que xhtml2pdf pueda acceder a ellas
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


def convert_to_pdf(template, filename, context={},):
    """
    Convierte una template pasada como argumento junto con el contexto dado a pdf.
    
    Args:
        template: Plantilla html a convertir a pdf
        filename: Nombre que tendrá el archivo convertido a .pdf
        contexto: Diccionario con los datos que se sustituirán en el html antes de la conversión

    Returns:
        bool: Valor de retorno. True en caso de éxito, False de otra forma
    """
    # Creamos el archivo que contendrá el pdf temporalmente
    archivo = open(str(settings.PDF_GEN_DIR) + '/' + filename, 'wb+')
    # Renderizamos la template con el contexto
    template = get_template(template)
    html = template.render(context)
    # Creamos el pdf y lo guardamos en el destino indicado anteriormente
    status = pisa.CreatePDF(html, dest=archivo, link_callback=link_callback)

    archivo.close()
    # Comprobamos si existen errores
    if status.err:
        return False

    return True


def date_format(date):
    """
    Función que transforma una fecha pasada por argumento en una cadena en español.

    Args:
        date: Objeto fecha sobre el cual se ejecutarán las operaciones

    Returns:
        string: Valor de retorno. Cadena con la fecha pasada por argumento en español.
    """
    # Separamos la fecha en componentes
    fecha = f'{date}'.split()[0]
    año, mes, dia = fecha.split('-')

    # Creamos un diccionario con los meses
    meses = {1: 'Enero', 2: 'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio', 7:'Julio', 
            8:'Agosto', 9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'}

    return "%s de %s del %s" % (dia, meses[int(mes)], año)