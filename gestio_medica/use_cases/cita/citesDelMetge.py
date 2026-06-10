from datetime import date
from gestio_medica.models import Cita


def citesDelMetge(dni_metge: str):
    avui = date.today()
    return list(
        Cita.objects.filter(
            dni_metge_id = dni_metge,
            data__gte    = avui
        ).exclude(
            estat = 'cancelada'
        ).order_by('data', 'hora')
    )
