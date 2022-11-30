from django.urls import path
from . import views

# Nombre de la app
app_name = 'firma_app'

# Enrutado
urlpatterns = [
    # Formulario para la firma
    path('', views.confirmacion_datos, name='firma-formulario'),
    path('datos-usuario/', views.confirmacion_datos, name='firma-datos'),
    path('pdf-generado/', views.pdf_usuario_sin_firma, name='solicitud-pdf'),
    path('pdf-firmado/', views.pdf_usuario_con_firma, name='firma-pdf')
]
