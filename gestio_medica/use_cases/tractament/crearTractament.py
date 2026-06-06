import re
from gestio_medica.models import Tractament, Diagnostic
from datetime import datetime


def crearTractament(codi_tractament, data_inici, data_fi_prevista, indicacions, codi_diagnostic):



    if not re.match(r'^TR\d{8}$', codi_tractament):
        raise ValueError("Error: El format del codi de tractament és incorrecte. Ha de ser 'TR' seguit de 8 dígits (Ex: TR00000001).")

    if not re.match(r'^DG\d{8}$', codi_diagnostic):
        raise ValueError("Error: El format del codi de diagnòstic és incorrecte. Ha de ser 'DG' seguit de 8 dígits (Ex: DG00000001).")

    if Tractament.objects.filter(codi_tractament = codi_tractament).exists():
        raise ValueError(f"Error: El tractament amb codi {codi_tractament} ja existeix en la BBDD.")
    
    try:
        diagnostic_obj = Diagnostic.objects.get(codi_diagnostic = codi_diagnostic)
    except Diagnostic.DoesNotExist:
        raise ValueError(f"Error: El diagnòstic amb codi {codi_diagnostic} no existeix en la BBDD.")
    
    try:
        d_inici = datetime.strptime(data_inici, '%Y-%m-%d').date() if isinstance(data_inici, str) else data_inici
        d_fi = datetime.strptime(data_fi_prevista, '%Y-%m-%d').date() if isinstance(data_fi_prevista, str) else data_fi_prevista
    except ValueError:
        raise ValueError("Error: El format de les dates ha de ser YYYY-MM-DD.")

    if d_fi < d_inici:
        raise ValueError("Error: La data de fi prevista no pot ser anterior a la data d'inici.")


    ntractament = Tractament.objects.create(
        codi_tractament = codi_tractament,
        data_inici = d_inici,
        data_fi_prevista = d_fi,
        indicacions = indicacions,
        diagnostic = diagnostic_obj  
    )

    return ntractament