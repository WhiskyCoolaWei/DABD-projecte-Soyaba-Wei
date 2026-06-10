from gestio_medica.models import EstocMedicament, Farmacia


def consultarEstocFarmacia(codi_centre: str):
    try:
        farmacia = Farmacia.objects.get(pk=codi_centre)
    except Farmacia.DoesNotExist:
        raise ValueError(f"Error: No existeix farmàcia al centre {codi_centre}.")

    estoc = (
        EstocMedicament.objects
        .filter(codi_centre=farmacia)
        .select_related('codi_nacional')
        .order_by('codi_nacional__nom_comercial')
    )
    return farmacia, list(estoc)
