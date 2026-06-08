from gestio_medica.models import Prescripcio

def llistarPrescripcions(codi_prescripcio=None, codi_tractament=None, codi_nacional=None, ordenar_per=None):
    queryset = Prescripcio.objects.all()
    
    # Filtres
    if codi_prescripcio:
        queryset = queryset.filter(codi_prescripcio__icontains=codi_prescripcio)
    if codi_tractament:
        queryset = queryset.filter(codi_tractament__icontains=codi_tractament)
    if codi_nacional:
        queryset = queryset.filter(codi_nacional__icontains=codi_nacional)
        
    # Lògica d'ordenació restringida només als camps de codis (ascendent i descendent)
    camps_admesos = [
        'codi_prescripcio', '-codi_prescripcio', 
        'codi_tractament', '-codi_tractament', 
        'codi_nacional', '-codi_nacional'
    ]
    
    if ordenar_per in camps_admesos:
        queryset = queryset.order_by(ordenar_per)
        
    return queryset