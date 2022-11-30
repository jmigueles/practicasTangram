window.addEventListener('load', inicio, true)

/**
 * Función inicio
 *  Inicializa el evento de click en el submit del formulario
 */
function inicio(){
    document.getElementById('enviar').addEventListener('click', validar, false);
}

/**
 * Función validar
 *  Esta función valida cada uno de los campos del formulario.
 *  Si todos están correctos y cumplen las restricciones se enviarán al servidor
 *  Si los campos no cumplen las restricciones se enviará un mensaje para el campo correspondiente.
 */
function validar(e){

    // Limpiamos campos
    document.getElementById('error_nombre').innerHTML = '';
    document.getElementById('error_dni').innerHTML = '';
    document.getElementById('error_texto').innerHTML = '';
    document.getElementById('error_apellido1').innerHTML = '';
    document.getElementById('error_apellido2').innerHTML = '';
    document.getElementById('error_manipulacion').innerHTML = '';
    
    // Expresiones regulares
    let regExpNomApe = /^[\sa-zA-ZñÑá-úÁ-Úä-ÿÄËÏÖÜ]{2,35}$/;
    let valido = true;

    // Datos del formulario
    const nombre = document.getElementById('id_nombre');
    console.log(nombre)
    const dni = document.getElementById('id_dni');
    const texto = document.getElementById('id_texto');
    const apellido1 = document.getElementById('id_primer_apellido');
    const apellido2 = document.getElementById('id_segundo_apellido');

    // Validaciones
    if(!regExpNomApe.test(nombre.value)){
        valido = false;
        document.getElementById('error_nombre').innerHTML = 'El nombre de usuario no es válido';
    }

    if(!regExpNomApe.test(apellido1.value))
    {
        valido = false;
        document.getElementById('error_apellido1').innerHTML = 'El primer apellido no es válido';
    }

    if(!regExpNomApe.test(apellido2.value))
    {
        valido = false;
        document.getElementById('error_apellido2').innerHTML = 'El segundo apellido no es válido';
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