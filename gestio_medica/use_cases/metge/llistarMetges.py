from gestio_medica.models import Metge

def llistarMetges(nom=None, cognoms=None, num_collegiat=None, ordenar_per=None):
    # Partim de tots els metges
    queryset = Metge.objects.all()
    
    # Apliquem filtres dinàmicament només si ens arriben dades
    if nom:
        # icontains fa que la cerca sigui parcial i ignori majúscules/minúscules
        queryset = queryset.filter(nom__icontains=nom)
    if cognoms:
        queryset = queryset.filter(cognoms__icontains=cognoms)
    if num_collegiat:
        queryset = queryset.filter(num_collegiat=num_collegiat)
        
    if ordenar_per:
        queryset = queryset.order_by(ordenar_per)
    
    return queryset