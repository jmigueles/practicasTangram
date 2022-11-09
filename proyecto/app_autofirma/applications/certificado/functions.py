import re
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO

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


'''
    convert_to_pdf(template, context={})
        Convierte una template pasada como argumento junto con el contexto dado a pdf.
'''
def convert_to_pdf(template, context={}):
    # Recogemos y renderizamos la template
    template = get_template(template)
    html = template.render(context)
    # Creamos un buffer en memoria para mostrarla al usuario y aplicamos codificación
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    
    # Comprobamos la existencia de errores
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return None

        