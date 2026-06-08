import re
from gestio_medica.models import Prescripcio

def crearPrescripcio(codi_prescripcio, codi_tractament, codi_nacional, dosi, frequencia, durada, estat='activa'):
    if not re.match(r'^PRE\d{8}$', codi_prescripcio):
        raise ValueError("Format incorrecte: El codi de prescripció ha de ser 'PRE' seguit de 8 dígits (Ex: PRE12345678).")
        
    # 2. Validar format de codi_tractament (TR seguido de exactamente 8 dígitos)
    if not re.match(r'^TR\d{8}$', codi_tractament):
        raise ValueError("Format incorrecte: El codi de tractament ha de ser 'TR' seguit de 8 dígits (Ex: TR12345678).")
        
    # 3. Validar format de codi_nacional (CN seguido de exactamente 6 dígitos)
    if not re.match(r'^CN\d{6}$', codi_nacional):
        raise ValueError("Format incorrecte: El codi nacional ha de ser 'CN' seguit de 6 dígits (Ex: CN123456).")

    # 4. Comprovar si ja existeix la prescripció
    if Prescripcio.objects.filter(codi_prescripcio=codi_prescripcio).exists():
        raise ValueError(f"Error: La prescripció amb codi {codi_prescripcio} ja existeix.")   
    nova_prescripcio = Prescripcio(
        codi_prescripcio=codi_prescripcio,
        codi_tractament=codi_tractament,
        codi_nacional=codi_nacional,
        dosi=dosi,
        frequencia=frequencia,
        durada=durada,
        estat=estat
    )
    nova_prescripcio.save()
    return nova_prescripcio