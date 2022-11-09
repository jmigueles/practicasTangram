window.addEventListener('load', inicio, true)

function inicio(){
    let palabra = 'hola';
    document.getElementById('enviar').addEventListener('click', validar, false);
}

function validar(e){

    // Limpiamos campos
    document.getElementById('error_nombre').innerHTML = '';
    document.getElementById('error_dni').innerHTML = '';
    document.getElementById('error_texto').innerHTML = '';
    document.getElementById('error_apellidos').innerHTML = '';
    document.getElementById('error_manipulacion').innerHTML = '';
    
    // Expresiones regulares
    let regExpNomApe = /^[\sa-zA-ZñÑá-úÁ-Úä-ÿÄËÏÖÜ]{2,35}$/;
    let valido = true;

    // Datos del formulario
    const nombre = document.getElementById('nombre_usuario');
    const dni = document.getElementById('dni_usuario');
    const texto = document.getElementById('texto_usuario');
    const apellidos = document.getElementById('apellidos_usuario');

    // Validaciones
    if(!regExpNomApe.test(nombre.value)){
        valido = false;
        document.getElementById('error_nombre').innerHTML = 'El nombre de usuario no es válido';
    }

    if(!regExpNomApe.test(apellidos.value))
    {
        valido = false;
        document.getElementById('error_apellidos').innerHTML = 'Los apellidos de usuario no son válidos';
    }
    
    if(!validarDNI(dni.value)){
        valido = false;
        document.getElementById('error_dni').innerHTML = 'El dni de usuario no es válido';
    }

    if(texto.value.length == 0 || texto.value.length > 512){
        valido = false;
        document.getElementById('error_texto').innerHTML = 'El texto es obligatorio y no puede exceder los 512 caracteres';
    }

    if(!valido) e.preventDefault()
}

function validarDNI(dni){
    let letras = 'TRWAGMYFPDXBNJZSQVHLCKET';
    let regexp = /^[XYZ]?\d{7,8}[A-Z]$/;
    let valido = false;

    if(regexp.test(dni)){
        let numero = dni.substring(0, dni.length-1);
    
        numero = numero.replace('X', 0);
        numero = numero.replace('Y', 1);
        numero = numero.replace('Z', 2);

        valido = letras[numero%23] === dni[dni.length-1];
    }

    //Sumamos los números 
    return valido
}