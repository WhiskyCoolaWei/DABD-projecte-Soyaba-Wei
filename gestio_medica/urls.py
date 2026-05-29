from django.urls import path
from . import views
from django.urls import path, include
urlpatterns = [
    # Cuando alguien entre en la URL raíz de la app, cargará la vista 'inicio'


    #======================================================================
    #======================================================================
                #ENDPOINTS PARA CASOS DE USO
    path('metges/', views.crearMetgeController, name = 'CrearMetge'),


    #======================================================================
    #======================================================================
]