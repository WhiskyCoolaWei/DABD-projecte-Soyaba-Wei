from gestio_medica.models import Malaltia


def crearMalaltia(codi_cie: str, nom: str, descripcio: str = ''):
    if Malaltia.objects.filter(pk=codi_cie).exists():
        raise ValueError(f"Error: Ja existeix una malaltia amb codi {codi_cie}.")
    if Malaltia.objects.filter(nom=nom).exists():
        raise ValueError(f"Error: Ja existeix una malaltia amb nom '{nom}'.")

    malaltia = Malaltia.objects.create(
        codi_cie=codi_cie, nom=nom, descripcio=descripcio)
    return malaltia