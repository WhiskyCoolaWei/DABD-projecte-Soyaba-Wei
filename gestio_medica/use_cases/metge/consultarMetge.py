from gestio_medica.models import Metge

def llistarMetges():
    return Metge.objects.all()

def consultarMetgePerDni(dni):
    try:
        return Metge.objects.get(dni=dni)
    except Metge.DoesNotExist:
        raise ValueError(f"Error: El metge amb DNI {dni} no existeix en la BBDD.")