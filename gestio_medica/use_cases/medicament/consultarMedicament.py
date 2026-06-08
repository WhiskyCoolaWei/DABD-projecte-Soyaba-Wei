from gestio_medica.models import Medicament

def consultarMedicament(filtre_nom=None, filtre_actiu=None):
    # Obtenemos todos los medicamentos ordenados alfabéticamente por nombre
    queryset = Medicament.objects.all().order_by('nom_comercial')
    
    # Aplicamos filtros si el usuario está buscando algo específico
    if filtre_nom:
        queryset = queryset.filter(nom_comercial__icontains=filtre_nom)
    if filtre_actiu:
        queryset = queryset.filter(principi_actiu__icontains=filtre_actiu)
        
    return queryset