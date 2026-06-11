from django.contrib.auth.hashers import check_password
from gestio_medica.models import Usuari, Metge, Pacient


def loginUsuari(email: str, contrasenya: str) -> dict:
    try:
        usuari = Usuari.objects.select_related('dni').get(email=email)
    except Usuari.DoesNotExist:
        raise ValueError("Error: Email o contrasenya incorrectes.")

    if not check_password(contrasenya, usuari.contrasenya):
        raise ValueError("Error: Email o contrasenya incorrectes.")

    persona = usuari.dni
    rols = []
    if Metge.objects.filter(pk=persona.dni).exists():
        rols.append('metge')
    if Pacient.objects.filter(pk=persona.dni).exists():
        rols.append('pacient')

    return {
        'dni' : persona.dni,
        'nom' : f'{persona.nom} {persona.cognoms}',
        'rols': rols,
    }