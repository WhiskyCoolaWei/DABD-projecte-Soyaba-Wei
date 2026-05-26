from django.urls import path
from . import views
from django.urls import path, include
urlpatterns = [
    # Cuando alguien entre en la URL raíz de la app, cargará la vista 'inicio'
    path('', views.inicio, name='inicio'),
    path('', include('gestio_medica.urls')),


    #======================================================================
    #======================================================================
                #ENDPOINTS PARA CASOS DE USO
    path('metges', views.crearMetgeController, name = 'CrearMetge'),


    #======================================================================
    #======================================================================
]