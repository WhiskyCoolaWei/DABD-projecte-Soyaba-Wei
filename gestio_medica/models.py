from django.db import models

# Create your models here.

#En la libreria models existe el metodo superclase Model que 
#nos permite que esta clase Persona se convierta en una tabla de datos PostgreSQL
#Basicamente con esto Django nos convierte la clase en una tabla de la BBDD, hace la conexion por nosotros

#En nuestra BBDD tenemos todas las tablas en minuscula, Django es sensible con las mayusculas y minusculas por lo que 
# aplicaremos una sub clase dentro de la clase tal que class meta: db_table = 'nombre-tabla' 
class Persona(models.Model):
    #CharField es un metodo de la libreria models 
    # y nos obliga a poner un max length en la variable creada
    # primary_key = True es para que Django no le asigne una ID aleatoria sino que 
    # se utilice el que hayamos asignado en nuestra bd
    dni = models.CharField(max_length = 9, primary_key = True)
    nom = models.CharField(max_length = 60)
    cognoms = models.CharField(max_length = 150)
    data_naixement = models.DateField()
    telefon = models.CharField(max_length = 20)
    adreca = models.CharField(max_length = 200)
    correu = models.CharField(max_length = 120, unique = True)

    class Meta:
        managed = False #Esto es para que Django no cree una nueva tabla, ya existe la nuestra
        db_table = 'persona'
    
    def __str__(self):
        return f"{self.nom} {self.cognoms}"
    
class Metge(Persona):
    persona_ptr = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE, # Requerido por Django en Python, no tocará PostgreSQL
        parent_link=True,
        db_column='dni',          # Nombre real de la columna FK en la tabla 'metge'
        primary_key=True          # El DNI también actúa como PK de esta tabla heredada
    )
    num_collegiat = models.CharField(max_length = 15, unique = True)
    
    class Meta:
        managed = False 
        db_table = 'metge'

class Pacient(Persona):
    persona_ptr = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE, # Requerido por Django en Python
        parent_link=True,
        db_column='dni',          # Nombre real de la columna FK en la tabla 'pacient'
        primary_key=True          # El DNI también actúa como PK aquí
    )
    class Meta:
        managed = False 
        db_table = 'pacient'

class Medicament(models.Model):
    codi_nacional = models.CharField(max_length = 15, primary_key = True)
    nom_comercial = models.CharField(max_length = 150)
    principi_actiu = models.CharField(max_length = 150)

    class Meta:
        managed = False 
        db_table = 'medicament'

    def __str__(self):
        return self.nom_comercial
    

class Cita(models.Model):
    ESTAT = [
        ('pendent', 'pendent'),
        ('confirmada','confirmada'),
        ('finalitzada','finalitzada'),
        ('cancelada','cancelada'),
    ]

    codi_cita = models.CharField(max_length = 15, primary_key = True)
    data = models.DateField()
    hora = models.TimeField()
    estat = models.CharField(max_length = 50, choices = ESTAT)
    dni_metge = models.ForeignKey('Metge', on_delete=models.CASCADE, db_column='dni_metge')
    dni_pacient = models.CharField(max_length=9)
    codi_centre = models.CharField(max_length=15)
    codi_sala = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'cita'
        
    def __str__(self):
        return self.codi_cita

class Diagnostic(models.Model):
    codi_diagnostic = models.CharField(max_length = 15, primary_key = True)
    descripcio = models.TextField()
    notes_cliniques = models.TextField(blank = True, null = True)

    #La clase cita no esta implementado, asi que para evitar errores lo 
    #dejaremos en un varchar temporal
    codi_cita = models.ForeignKey(Cita, on_delete = models.CASCADE, db_column = 'dni_metge')

    class Meta:
        managed = False
        db_table = 'diagnostic'

    def __str__(self):
        return self.codi_diagnostic
    

    
class Tractament(models.Model):
    codi_tractament = models.CharField(max_length = 15, primary_key = True)
    data_inici = models.DateField()
    data_fi_prevista = models.DateField()
    indicacions = models.TextField(blank = True, null = True)

    #añadimos diagnostic
    diagnostic = models.ForeignKey(
        Diagnostic,
        on_delete = models.CASCADE,
        db_column = 'codi_diagnostic'
    )

    class Meta:
        managed = False 
        db_table = 'tractament'

    def __str__(self):
        return self.codi_tractament

class Prescripcio(models.Model):
    codi_prescripcio = models.CharField(max_length = 15, primary_key = True)
    tractament = models.ForeignKey(Tractament, on_delete = models.CASCADE)
    medicament = models.ForeignKey(Medicament, on_delete = models.CASCADE)

    dosi = models.CharField(max_length = 60)
    frequencia = models.CharField(max_length = 60)
    durada = models.CharField(max_length = 60)
    estat = models.CharField(max_length = 20)

    class Meta:
        managed = False
        db_table = 'prescripcio'

