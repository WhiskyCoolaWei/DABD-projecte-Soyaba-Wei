import re
from gestio_medica.models import Pacient, Persona

def crearPacient(dni, nom, cognoms, data_naixement, telefon, adreca, correu):
    
    if not re.match(r'^\d{8}[A-Z]$', dni):
        raise ValueError("Error: El format del DNI és incorrecte. Ha de contenir 8 dígits i una lletra majúscula (Ex: 12345678Z).")
    
    if Pacient.objects.filter(dni=dni).exists():
        raise ValueError(f"Error: Ja existeix un pacient registrat amb el DNI {dni}.")
        
    if Persona.objects.filter(correu=correu).exists():
        raise ValueError(f"Error: El correu electrònic '{correu}' ja està registrat per un altre usuari.")

    nou_pacient = Pacient.objects.create(
        dni=dni,
        nom=nom,
        cognoms=cognoms,
        data_naixement=data_naixement,
        telefon=telefon,
        adreca=adreca,
        correu=correu
    )
    return nou_pacient