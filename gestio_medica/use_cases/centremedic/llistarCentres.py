from gestio_medica.models import CentreMedic


def llistarCentres():
    return list(CentreMedic.objects.all().order_by('nom'))
