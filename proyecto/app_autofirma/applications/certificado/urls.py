from django.urls import path
from . import views

# Nombre de la app
app_name = 'firma_app'

# Enrutado
urlpatterns = [
    # Formulario para la firma
    path('', views.Formulario_solicitud.as_view(), name='firma-formulario'),
    path('datos_usuario/', views.confirmacion_datos, name='firma-datos'),
    path('pdf-generado/', views.pdf_usuario, name='firma-pdf'),
]
