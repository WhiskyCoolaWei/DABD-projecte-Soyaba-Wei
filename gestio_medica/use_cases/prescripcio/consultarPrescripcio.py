from gestio_medica.models import Prescripcio

def consultarPrescripcioPerCodi(codi_prescripcio):
    try:
        return Prescripcio.objects.get(codi_prescripcio=codi_prescripcio)
    except Prescripcio.DoesNotExist:
        raise ValueError(f"Error: La prescripció amb codi {codi_prescripcio} no existeix en la BBDD.")