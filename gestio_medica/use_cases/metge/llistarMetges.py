from gestio_medica.models import Metge

def llistarMetges():
    return Metge.objects.all()