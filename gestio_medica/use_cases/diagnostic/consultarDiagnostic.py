from gestio_medica.models import Diagnostic

def consultarDiagnosticPerCodi(codi_diagnostic):
    try:
        return Diagnostic.objects.get(codi_diagnostic=codi_diagnostic)
    except Diagnostic.DoesNotExist:
        raise ValueError(f"Error: El diagnòstic amb codi {codi_diagnostic} no existeix.")