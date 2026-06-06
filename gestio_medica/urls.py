from django.urls import path


from gestio_medica.views.viewsMetge import crearMetgeController
from gestio_medica.views.viewsTractament import crearTractamentController
from gestio_medica.views.viewsTractament import consultarTractamentController
from gestio_medica.views.viewsDiagnostic import crearDiagnosticController

from django.urls import path, include
urlpatterns = [
    # Cuando alguien entre en la URL raíz de la app, cargará la vista 'inicio'


    #======================================================================
    #======================================================================
                #ENDPOINTS PARA CASOS DE USO
    path('metges/', crearMetgeController, name = 'CrearMetge'),

    path('tractaments/', crearTractamentController, name = 'crearTractament'),

    path('tractaments/consultar/', consultarTractamentController, name='ConsultarTractament'),

    path('diagnostics/', crearDiagnosticController, name='CrearDiagnostic'),
    #======================================================================
    #======================================================================
]