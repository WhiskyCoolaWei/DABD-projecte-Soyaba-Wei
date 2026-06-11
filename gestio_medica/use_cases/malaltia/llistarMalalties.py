from gestio_medica.models import Malaltia


def llistarMalalties(cerca: str = ''):
    qs = Malaltia.objects.all().order_by('nom')
    if cerca:
        qs = qs.filter(nom__icontains=cerca) | \
             Malaltia.objects.filter(codi_cie__icontains=cerca)
    return list(qs)