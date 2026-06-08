from gestio_medica.models import Pacient

def consultarPacientPerDni(dni):
    try:
        return Pacient.objects.get(dni=dni)
    except Pacient.DoesNotExist:
        raise ValueError(f"Error: No s'ha trobat cap pacient amb el DNI '{dni}' a la base de dades.")