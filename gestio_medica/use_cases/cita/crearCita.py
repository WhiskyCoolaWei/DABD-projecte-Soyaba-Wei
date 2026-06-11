import re
from gestio_medica.models import Cita, Metge

def crearCita(codi_cita, data, hora, estat, dni_metge, dni_pacient, codi_centre, codi_sala):
    if not re.match(r'^CT\d{8}$', codi_cita):
        raise ValueError("Error: El format del codi de cita és incorrecte. Ha de ser 'CT' seguit de 8 dígits.")
    
    if Cita.objects.filter(codi_cita=codi_cita).exists():
        raise ValueError(f"Error: La cita amb codi {codi_cita} ja existeix en la BBDD.")
        
    if not Metge.objects.filter(dni=dni_metge).exists():
        raise ValueError(f"Error: El metge amb DNI {dni_metge} no existeix en la BBDD.")
    
    metge_instancia = Metge.objects.get(dni=dni_metge)

    # Un metge no pot crear una cita per a si mateix com a pacient
    if dni_pacient == dni_metge:
        raise ValueError("Error: Un metge no es pot assignar una cita a si mateix com a pacient.")
    
    ncita = Cita.objects.create(
        codi_cita=codi_cita,
        data=data,
        hora=hora,
        estat=estat,
        dni_metge=metge_instancia,
        dni_pacient=dni_pacient,
        codi_centre=codi_centre,
        codi_sala=codi_sala
    )
    return ncita