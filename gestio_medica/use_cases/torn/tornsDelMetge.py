from django.utils import timezone
from gestio_medica.models import Torn


DIES_NOM = {1:'Dilluns', 2:'Dimarts', 3:'Dimecres',
            4:'Dijous',  5:'Divendres', 6:'Dissabte', 7:'Diumenge'}


def tornsDelMetge(dni_metge: str, codi_centre: str = None):
    avui = timezone.now().date()
    qs = Torn.objects.filter(
        dni_metge=dni_metge,
        data_fi__gte=avui          # nomes torns vigents
    ).select_related('codi_centre').order_by('dia_setmana', 'hora_inici')
    if codi_centre:
        qs = qs.filter(codi_centre=codi_centre)
    return list(qs)
