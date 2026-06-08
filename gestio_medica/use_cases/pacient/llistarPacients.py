from django.db.models import Subquery, OuterRef, Count, Value
from django.db.models.functions import Coalesce
from gestio_medica.models import Pacient, Cita

def llistarPacients(dni=None, nom=None, cognoms=None, ordenar_per=None):
    # Creamos una subconsulta para contar las citas activas de cada paciente
    # Definimos como activas las que están 'pendent' o 'confirmada'
    citas_subquery = Cita.objects.filter(
        dni_pacient=OuterRef('dni'),
        estat__in=['pendent', 'confirmada']
    ).values('dni_pacient').annotate(count=Count('codi_cita')).values('count')

    # Anotamos el QuerySet de Pacientes con el resultado de la subconsulta
    # Usamos Coalesce para que si un paciente tiene 0 citas, devuelva un 0 en vez de None
    queryset = Pacient.objects.annotate(
        citas_activas=Coalesce(Subquery(citas_subquery), Value(0))
    )
    
    # 3. Aplicamos los filtros comunes si vienen informados (búsqueda parcial)
    if dni:
        queryset = queryset.filter(dni__icontains=dni)
    if nom:
        queryset = queryset.filter(nom__icontains=nom)
    if cognoms:
        queryset = queryset.filter(cognoms__icontains=cognoms)
        
    # Control de ordenación (incluyendo el nuevo orden por citas activas)
    # Puede recibir 'citas_activas' (Ascendente) o '-citas_activas' (Descendente)
    if ordenar_per:
        queryset = queryset.order_by(ordenar_per)
    else:
        queryset = queryset.order_by('cognoms', 'nom') # Orden por defecto
        
    return queryset