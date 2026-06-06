from gestio_medica.models import Tractament


def consultarTractament(codi_tractament):
    try:
        tractament = Tractament.objects.get(codi_tractament=codi_tractament)
        
        dades = {
            "codi_tractament": tractament.codi_tractament,
            "data_inici": tractament.data_inici.strftime("%Y-%m-%d"),
            "data_fi_prevista": tractament.data_fi_prevista.strftime("%Y-%m-%d"),
            "indicacions": tractament.indicacions,
            "codi_diagnostic": tractament.diagnostic.codi_diagnostic
        }
        
        return dades
        
    except Tractament.DoesNotExist:
        raise ValueError(f"Error: El tractament amb codi {codi_tractament} no existeix a la BBDD.")