# Imports de django
from django import forms

# Models
from .models import Usuario

# Librerías de python
import re


# Formulario de registro de solicitud
class SolicitudForm(forms.Form):
    """
    SolicitudForm: Formulario de inserción de datos de solicitud por parte del usuario.

    Nota:
        Cada uno de los campos que se describen a continuación tiene su respectivo
        'clean' más abajo encargado de filtrar los datos de forma correcta.

    Campos:
        nombre (str): Campo de tipo texto para almacenar el nombre
        primer_apellido (str): Campo de tipo texto para almacenar el primer apellido
        segundo_apellid (str): Campo de tipo texto para almacenar el segundo apellido
        dni (str): Campo de tipo texto para almacenar el dni
        texto (str): Campo de tipo texto para almacenar el texto
    """
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={ 'placeholder':'Introduzca su nombre...', 'class':'form-control' }
        )
    )

    primer_apellido = forms.CharField(
        widget=forms.TextInput(
            attrs={ 'placeholder':'Introduzca primer apellido...', 'class':'form-control' }
        )
    )

    segundo_apellido = forms.CharField(
        widget=forms.TextInput(
            attrs={ 'placeholder':'Introduzca segundo apellido...', 'class':'form-control' }
        )
    )

    dni = forms.CharField(
        widget=forms.TextInput(
            attrs={ 'placeholder':'Introduzca su dni...', 'class':'form-control'}
        )
    )

    texto = forms.CharField(
        widget=forms.Textarea(
            attrs={ 'placeholder':'Introduzca el texto de su solicitud aquí...', 'class':'form-control', 'rows':'3' }
        )
    )

    # Validaciones
    def clean_nombre(self):
        regExp = "^[\sa-zA-ZñÑá-úÁ-Úä-ÿÄËÏÖÜ]{2,35}$" 
        nombre = str.strip(self.cleaned_data['nombre'])

        if not re.match(regExp, nombre ):
            self.add_error('nombre', forms.ValidationError('El nombre no es válido'))

        return nombre

    def clean_primer_apellido(self):
        regExp = "^[\sa-zA-ZñÑá-úÁ-Úä-ÿÄËÏÖÜ]{2,35}$" 
        apellido1 = str.strip(self.cleaned_data['primer_apellido'])

        if not re.match(regExp, apellido1):
            self.add_error('primer_apellido', forms.ValidationError('El primer apellido no es válido'))

        return apellido1

    def clean_segundo_apellido(self):
        regExp = "^[\sa-zA-ZñÑá-úÁ-Úä-ÿÄËÏÖÜ]{2,35}$"
        apellido2 = str.strip(self.cleaned_data['segundo_apellido'])

        if not re.match(regExp, apellido2):
            self.add_error('segundo_apellido', forms.ValidationError('El segundo apellido no es válido'))

        return apellido2

    def clean_dni(self):
        # Letras para comprobar la validez del caracter
        letras = 'TRWAGMYFPDXBNJZSQVHLCKET'
        regExp = "^[XYZ]?\d{7,8}[A-Z]$"
        dni = str.strip(self.cleaned_data['dni'])
        
        valido = False

        # Validaciones
        if re.match("^[XYZ]?\d{7,8}[A-Z]$", dni):
            numero = dni[0:len(dni)-1]
            numero = numero.replace('X', '0')
            numero = numero.replace('Y', '1')
            numero = numero.replace('Z', '2')

            # Comprobamos si cumple la lógica
            valido = letras[int(numero)%23] == dni[len(dni)-1]    

        if not valido: self.add_error('dni', 'El dni no es válido')
        
        return dni

    def clean_texto(self):
        texto = str.strip(self.cleaned_data['texto'])

        if len(texto) == 0 or len(texto) > 512:
            self.add_error('texto', forms.ValidationError('El texto es obligatorio y no puede exceder los 512 caracteres'))

        return texto
