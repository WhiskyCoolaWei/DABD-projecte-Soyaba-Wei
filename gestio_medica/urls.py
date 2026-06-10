from django.urls import path
from gestio_medica.views.viewsMetge import crearMetgeController
from gestio_medica.views.viewsTractament import crearTractamentController, consultarTractamentController
from gestio_medica.views.viewsDiagnostic import crearDiagnosticController
from gestio_medica.views.viewsCita import crearCitaController
from gestio_medica.views.viewsPrescripcio import prescripcioController
from gestio_medica.views.viewsPacient import pacientController
from gestio_medica.views.viewsHistorialClinic import historialClinicController
from gestio_medica.views.viewsMedicament import medicamentController
from gestio_medica.views.viewsUsuari import usuariController, loginController
from gestio_medica.views.viewsMalaltia import malaltiaController, associarMalaltiaController
from gestio_medica.views.viewsSupervisio import supervisioController
from gestio_medica.views.viewsCentreMedic import centreMedicController
from gestio_medica.views.viewsTorn import tornController

urlpatterns = [
    #======================================================================
    # ENDPOINTS PARA CASOS DE USO — Part Wei
    path('metges/', crearMetgeController, name='CrearMetge'),
    path('tractaments/', crearTractamentController, name='crearTractament'),
    path('tractaments/consultar/', consultarTractamentController, name='ConsultarTractament'),
    path('diagnostics/', crearDiagnosticController, name='CrearDiagnostic'),
    path('cites/', crearCitaController, name='CrearCita'),
    path('prescripcions/', prescripcioController, name='Prescripcio'),
    path('pacients/', pacientController, name='gestio_pacients'),
    path('historial/', historialClinicController, name='consultar_historial'),
    path('medicaments/', medicamentController, name='gestio_medicaments'),
    # ── Part Soyaba ───────────────────────────────────────────────────────
    path('usuaris/', usuariController, name='CrearUsuari'),
    path('login/', loginController, name='Login'),
    path('malalties/', malaltiaController, name='Malalties'),
    path('diagnostics/<str:codi_diagnostic>/malalties/', associarMalaltiaController, name='AssociarMalaltia'),
    path('supervisio/', supervisioController, name='Supervisio'),
    path('centres/', centreMedicController, name='Centres'),
    path('torns/', tornController, name='Torns'),
    #======================================================================
]
