window.addEventListener('load', inicio, true)

/**
 * Función inicio:
 *  Inicializa el evento de click en el botón de continuar para que lance una ventana
 *  diálogo al usuario
 */
function inicio(e)
{
    document.getElementById("continuar").addEventListener('click', function(e){
        if(confirm('¿Quiere generar un pdf con los datos introducidos?'))
        {
            document.getElementById("form").submit()
        }else
        {
            e.preventDefault()
        }
    }, false)
}