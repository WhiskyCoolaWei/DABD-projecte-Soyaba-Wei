from gestio_medica.models import Persona, Metge
#No instanciamos ni declaramos librerias, trabajamos con las entities declaradas en models.py

def crearMetge(dni, nom, cognoms, data_naixement, telefon, adreca, correu, num_collegiat):
    if Persona.objects.filter(dni = dni).exists():
       #Usamos raise ValueError en vez de un Printf porque este para el programa si hay error
       raise ValueError(f"Error: L'usuari amb DNI {dni} ja existeix en la BBDD.")
    
    if len(dni) != 9:
        raise ValueError(f"Error: DNI invalid: Mida incorrecta")
    
    if Metge.objects.filter(num_collegiat = num_collegiat).exists():
        raise ValueError(f"Número de collegiat ja existent en la BBDD")
    
#NO HE INCLUIDO ESPECIALITAT PORQUE NO ESTA IMPLICITAMENTE PUESTO COMO ATRIBUTO
#EN LA CLASE MEDICO
    nmetge = Metge.objects.create(
        dni = dni,
        nom = nom,
        cognoms = cognoms,
        data_naixement = data_naixement,
        telefon = telefon,
        adreca = adreca,
        correu = correu,
        num_collegiat = num_collegiat
    )

    return nmetge