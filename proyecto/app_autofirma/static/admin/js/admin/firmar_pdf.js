window.addEventListener('load', inicio, true)

function inicio()
{
    document.getElementById('autofirma').addEventListener('click', firmar, false)
}

function firmar()
{
    if (confirm('¿Quiere validar el documento?'))
    {
        alert('Fin app v1')
    }else
    {
        location.href='http://tangramafirma.es:9000'
    }
}