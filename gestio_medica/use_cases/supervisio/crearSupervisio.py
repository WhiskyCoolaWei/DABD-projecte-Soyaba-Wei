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
    """Retorna els supervisors del metge donat.

    Regla d'aplicacio (jerarquia de dos nivells): un metge que ja
    supervisa a algu (es a dir, es senior) mai pot tenir supervisors
    propis. Si el metge consultat te alguna fila com a dni_supervisor,
    es considera senior i es retorna llista buida encara que la BD
    tingui (per dades antigues) alguna fila on tambe figuri com a
    supervisat.
    """
    try:
        supervisat = Metge.objects.get(pk=dni_supervisat)
    except Metge.DoesNotExist:
        raise ValueError(f"Error: No existeix cap metge amb DNI {dni_supervisat}.")

    es_senior = Supervisio.objects.filter(dni_supervisor=supervisat).exists()
    if es_senior:
        return []

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
