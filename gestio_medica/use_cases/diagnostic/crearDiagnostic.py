import re
from gestio_medica.models import Diagnostic, Cita  # <-- Importem també la Cita

def crearDiagnostic(codi_diagnostic, descripcio, notes_cliniques, codi_cita):
    # 1. Validació del format del codi de diagnòstic
    if not re.match(r'^DG\d{8}$', codi_diagnostic):
        raise ValueError("Error: El format del codi de diagnòstic és incorrecte. Ha de ser 'DG' seguit de 8 dígits.")
    
    # 2. Validació de duplicats del diagnòstic
    if Diagnostic.objects.filter(codi_diagnostic=codi_diagnostic).exists():
        raise ValueError(f"Error: El diagnòstic amb codi {codi_diagnostic} ja existeix en la BBDD.")
    
    # 3. NOVA VALIDACIÓ: Control de Cita inexistent
    if not Cita.objects.filter(codi_cita=codi_cita).exists():
        raise ValueError(f"Error: La cita amb codi '{codi_cita}' no existeix a la base de dades. Comprova que sigui correcta.")
    
    # Si totes les barreres de negoci es passen correctament, creem el registre
    ndiagnostic = Diagnostic.objects.create(
        codi_diagnostic=codi_diagnostic,
        descripcio=descripcio,
        notes_cliniques=notes_cliniques,
        codi_cita_id=codi_cita
    )
    return ndiagnostic