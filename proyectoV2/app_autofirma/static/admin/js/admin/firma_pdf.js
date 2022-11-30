window.addEventListener('load', iniciar, true);

/**
 * Función iniciar.
 *  Inicializa el evento de click en el botón de firma en el html.
 */
function iniciar()
{
    document.getElementById('autofirma').addEventListener('click', firmarDocumento, false)
}

/**
 * Función firmarDocumento.
 *  Carga el autoscript de autofirma e inicia la aplicación en el equipo del cliente.
 *  Se establecen una serie de parámetros para ubicar la firma y se envían los datos 
 *  al servidor al terminar.
 */
function firmarDocumento()
{
    // Si el usuario no quiere validar el documento se le retonará al inicio
    if (confirm('¿Quiere validar el documento?'))
    {
        AutoScript.cargarAppAfirma();

        // Parámetros para posicionar la firma
        let extraParams = "signaturePositionOnPageLowerLeftX=100\n" + 
                          "signaturePositionOnPageLowerLeftY=250\n" +
                          "signaturePositionOnPageUpperRightX=550\n" +
                          "signaturePositionOnPageUpperRightY=550\n" +
                          "signaturePage=1\n" +
                          "layer2Text=Firmado por $$SUBJECTCN$$ el día $$SIGNDATE=dd/MM/yyyy$$ " +
                          "con certificado emitido por AC FNMT Usuarios"

        // Función de firmado
        function enviarFirma(firma, certificado)
        {
            // Firma y certificado para el servidor
            document.getElementById('firma').value = firma
            document.getElementById('certificado').value = certificado

            // Enviamos el formulario al servidor
            document.getElementById('form').submit()
        }

        // Función de 
        function mostrarError(type, message)
        {
            showError(message);
        }

        // Obtenemos el documento pdf del servidor y lo preparamos para la firma en base64
        pdf = document.getElementById('pdf_base64').value.slice(2, document.getElementById('pdf_base64').value.length-1)
        
        // Iniciamos el cliente autfirma
        AutoScript.sign(pdf, "SHA256withRSA", "PAdES", extraParams, enviarFirma, mostrarError)
    }else
    {   
        // Inicio de la app 
        location.href='http://tangramafirma.es:9000'
    }
}