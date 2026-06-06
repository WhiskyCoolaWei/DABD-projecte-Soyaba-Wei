import re
from gestio_medica.models import Diagnostic

def crearDiagnostic(codi_diagnostic, descripcio, notes_cliniques, codi_cita):
    if not re.match(r'^DG\d{8}$', codi_diagnostic):
        raise ValueError("Error: El format del codi de diagnòstic és incorrecte. Ha de ser 'DG' seguit de 8 dígits.")
    
    if Diagnostic.objects.filter(codi_diagnostic=codi_diagnostic).exists():
        raise ValueError(f"Error: El diagnòstic amb codi {codi_diagnostic} ja existeix en la BBDD.")
    
    ndiagnostic = Diagnostic.objects.create(
        codi_diagnostic=codi_diagnostic,
        descripcio=descripcio,
        notes_cliniques=notes_cliniques,
        codi_cita=codi_cita
    )
    return ndiagnostic