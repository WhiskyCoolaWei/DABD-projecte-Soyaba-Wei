from datetime import datetime, timedelta
from gestio_medica.models import Cita, Torn


def slotsDisponibles(dni_metge: str, data_str: str, codi_centre: str):
    """Retorna llista d'hores lliures (cada hora) per un metge, data i centre."""
    data     = datetime.strptime(data_str, '%Y-%m-%d').date()
    dia_bd   = data.isoweekday()   # 1=Dilluns...7=Diumenge, igual que la BD

    # Torns vigents aquell dia concret
    torns = Torn.objects.filter(
        dni_metge_id   = dni_metge,
        codi_centre_id = codi_centre,
        dia_setmana    = dia_bd,
        data_inici__lte= data,
        data_fi__gte   = data
    )
    if not torns.exists():
        return []

    # Hores ja ocupades (cites actives aquell dia)
    ocupades = set(
        Cita.objects.filter(
            dni_metge_id = dni_metge,
            data         = data
        ).exclude(estat='cancelada').values_list('hora', flat=True)
    )

    # Genera slots d'1h per cada torn i filtra les ocupades
    lliures = []
    for torn in torns:
        cursor = datetime.combine(data, torn.hora_inici)
        fi     = datetime.combine(data, torn.hora_fi)
        while cursor < fi:
            hora = cursor.time()
            if hora not in ocupades:
                lliures.append(hora.strftime('%H:%M'))
            cursor += timedelta(hours=1)

    return sorted(set(lliures))
