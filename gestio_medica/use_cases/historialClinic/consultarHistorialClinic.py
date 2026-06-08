from gestio_medica.models import HistorialClinic, Cita

def consultarHistorialClinic(dni_pacient, dni_metge=None):
    # Buscamos la ficha base del historial clínico
    try:
        historial = HistorialClinic.objects.get(dni_pacient=dni_pacient)
    except HistorialClinic.DoesNotExist:
        raise ValueError(f"Error: No s'ha trobat cap historial clínic vinculat al DNI '{dni_pacient}'.")
    
    # Empezamos con todas las citas del paciente
    cites = Cita.objects.filter(dni_pacient=dni_pacient)
    
    # 🆕 Si nos pasan el DNI del médico, filtramos la consulta
    if dni_metge:
        cites = cites.filter(dni_metge=dni_metge)
        
    # Ordenamos de más reciente a más antigua
    cites = cites.order_by('-data', '-hora')
    
    return historial, cites