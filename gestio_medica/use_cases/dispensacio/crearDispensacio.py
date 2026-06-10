import uuid
from datetime import date
from gestio_medica.models import Dispensacio, Farmacia, Prescripcio, EstocMedicament


def crearDispensacio(codi_centre: str, codi_tractament: str,
                     codi_nacional: str, quantitat: int):
    # Farmàcia ha d'existir
    try:
        farmacia = Farmacia.objects.get(pk=codi_centre)
    except Farmacia.DoesNotExist:
        raise ValueError(f"Error: No existeix farmàcia al centre {codi_centre}.")

    # La prescripció ha d'existir i estar activa (el trigger RS5 ho re-comprova)
    presc = Prescripcio.objects.filter(
        codi_tractament=codi_tractament,
        codi_nacional=codi_nacional
    ).first()
    if not presc:
        raise ValueError("Error: No existeix cap prescripció amb aquest tractament i medicament.")
    if presc.estat != 'activa':
        raise ValueError(f"Error: La prescripció no està activa (estat: {presc.estat}).")

    # Comprovar estoc disponible
    estoc = EstocMedicament.objects.filter(
        codi_centre=farmacia,
        codi_nacional=codi_nacional
    ).first()
    if not estoc:
        raise ValueError("Error: La farmàcia no té aquest medicament a l'estoc.")
    if estoc.quantitat_disponible < quantitat:
        raise ValueError(
            f"Error: Estoc insuficient. Disponible: {estoc.quantitat_disponible}, sol·licitat: {quantitat}."
        )

    # Crear la dispensació (el trigger de la BD decrementa l'estoc)
    nova = Dispensacio.objects.create(
        codi_dispensacio     = f'DIS{uuid.uuid4().hex[:9].upper()}',
        data_lliurament      = date.today(),
        quantitat_dispensada = quantitat,
        codi_centre          = farmacia,
        codi_tractament      = codi_tractament,
        codi_nacional        = codi_nacional,
    )
    return nova
