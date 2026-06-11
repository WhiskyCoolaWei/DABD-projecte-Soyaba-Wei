from gestio_medica.models import Metge, Supervisio


def crearSupervisio(dni_supervisor: str, dni_supervisat: str):
    if dni_supervisor == dni_supervisat:
        raise ValueError("Error: Un metge no es pot supervisar a si mateix.")

    try:
        supervisor = Metge.objects.get(pk=dni_supervisor)
    except Metge.DoesNotExist:
        raise ValueError(f"Error: No existeix cap metge amb DNI {dni_supervisor}.")

    try:
        supervisat = Metge.objects.get(pk=dni_supervisat)
    except Metge.DoesNotExist:
        raise ValueError(f"Error: No existeix cap metge amb DNI {dni_supervisat}.")

    if Supervisio.objects.filter(
            dni_supervisor=supervisor, dni_supervisat=supervisat).exists():
        raise ValueError("Aquesta relació de supervisió ja existeix.")

    Supervisio.objects.create(
        dni_supervisor=supervisor,
        dni_supervisat=supervisat)
    return supervisor, supervisat


def supervisorsDe(dni_supervisat: str):
    try:
        supervisat = Metge.objects.get(pk=dni_supervisat)
    except Metge.DoesNotExist:
        raise ValueError(f"Error: No existeix cap metge amb DNI {dni_supervisat}.")

    return list(
        Supervisio.objects
        .filter(dni_supervisat=supervisat)
        .select_related('dni_supervisor')
    )


def supervisatsDe(dni_supervisor: str):
    try:
        supervisor = Metge.objects.get(pk=dni_supervisor)
    except Metge.DoesNotExist:
        raise ValueError(f"Error: No existeix cap metge amb DNI {dni_supervisor}.")

    return list(
        Supervisio.objects
        .filter(dni_supervisor=supervisor)
        .select_related('dni_supervisat')
    )
