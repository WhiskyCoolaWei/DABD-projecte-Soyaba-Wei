from gestio_medica.models import Cita

def consultarCita(codi_cita):
    try:
        cita_instancia = Cita.objects.get(codi_cita=codi_cita)
        return cita_instancia
    except Cita.DoesNotExist:
        raise ValueError(f"Error: La cita amb codi {codi_cita} no existeix en la BBDD.")