import uuid
from django.contrib.auth.hashers import make_password
from gestio_medica.models import Usuari, Persona


def crearUsuari(email: str, contrasenya: str, dni: str):
    if Usuari.objects.filter(email=email).exists():
        raise ValueError(f"Error: L'email {email} ja està registrat.")

    try:
        persona = Persona.objects.get(pk=dni)
    except Persona.DoesNotExist:
        raise ValueError(f"Error: No existeix cap persona amb DNI {dni}.")

    if Usuari.objects.filter(dni=persona).exists():
        raise ValueError(f"Error: Aquesta persona ja té un usuari creat.")

    nou_usuari = Usuari.objects.create(
        codi_usuari = f'USR{uuid.uuid4().hex[:9].upper()}',
        email       = email,
        contrasenya = make_password(contrasenya),
        dni         = persona,
    )
    return nou_usuari
