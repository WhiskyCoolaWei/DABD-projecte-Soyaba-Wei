from gestio_medica.models import Diagnostic, Malaltia, DiagnosticMalaltia


def associarMalaltiaADiagnostic(codi_diagnostic: str, codi_cie: str):
    try:
        diagnostic = Diagnostic.objects.get(pk=codi_diagnostic)
    except Diagnostic.DoesNotExist:
        raise ValueError(f"Error: Diagnòstic {codi_diagnostic} no trobat.")

    try:
        malaltia = Malaltia.objects.get(pk=codi_cie)
    except Malaltia.DoesNotExist:
        raise ValueError(f"Error: Malaltia {codi_cie} no trobada.")

    if DiagnosticMalaltia.objects.filter(
            diagnostic=diagnostic, malaltia=malaltia).exists():
        raise ValueError("Aquesta malaltia ja està associada a aquest diagnòstic.")

    DiagnosticMalaltia.objects.create(diagnostic=diagnostic, malaltia=malaltia)
    return malaltia


def malaltiesDeDiagnostic(codi_diagnostic: str):
    try:
        diagnostic = Diagnostic.objects.get(pk=codi_diagnostic)
    except Diagnostic.DoesNotExist:
        raise ValueError(f"Error: Diagnòstic {codi_diagnostic} no trobat.")

    return list(
        DiagnosticMalaltia.objects
        .filter(diagnostic=diagnostic)
        .select_related('malaltia')
    )
