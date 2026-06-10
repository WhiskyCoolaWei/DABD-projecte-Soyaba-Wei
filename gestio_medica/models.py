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

    # Relación real con la tabla Cita
    codi_cita = models.ForeignKey(
        Cita, 
        on_delete = models.CASCADE, 
        db_column = 'codi_cita'
    )
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
    ESTAT = [
        ('activa', 'activa'),
        ('finalitzada', 'finalitzada'),
    ]

    codi_prescripcio = models.CharField(max_length = 15, primary_key = True)
    codi_tractament = models.CharField(max_length = 15)
    codi_nacional = models.CharField(max_length = 15)
    dosi = models.CharField(max_length = 60)
    frequencia = models.CharField(max_length = 60)
    durada = models.CharField(max_length = 60)
    estat = models.CharField(max_length = 50, choices = ESTAT, default = 'activa')

    class Meta:
        managed = False
        db_table = 'prescripcio'
    
    def __str__(self):
        return f"Prescripció {self.codi_prescripcio} - Tractament {self.codi_tractament}"

class HistorialClinic(models.Model):
    codi_historial = models.CharField(max_length =15, primary_key =True)
    dni_pacient = models.OneToOneField('Pacient', on_delete = models.CASCADE, db_column ='dni_pacient')
    allergies = models.TextField(blank = True, null = True)
    grup_sanguini = models.CharField(max_length=3, blank=True, null=True)
    antecedents = models.TextField(blank=True, null=True)
    malalties_croniques = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historialclinic'

class Usuari(models.Model):
    codi_usuari = models.CharField(max_length=15, primary_key=True)
    email       = models.CharField(max_length=100, unique=True)
    contrasenya = models.CharField(max_length=255)
    dni         = models.OneToOneField(
                    Persona,
                    on_delete=models.CASCADE,
                    db_column='dni',
                    related_name='usuari')

    class Meta:
        managed  = False
        db_table = 'usuari'

    def __str__(self):
        return self.email


class Malaltia(models.Model):
    codi_cie   = models.CharField(max_length=10, primary_key=True)
    nom        = models.CharField(max_length=150, unique=True)
    descripcio = models.TextField(blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'malaltia'

    def __str__(self):
        return f"{self.codi_cie} - {self.nom}"


class DiagnosticMalaltia(models.Model):
    diagnostic = models.ForeignKey(
                    Diagnostic,
                    on_delete=models.CASCADE,
                    db_column='codi_diagnostic',
                    related_name='malalties')
    malaltia   = models.ForeignKey(
                    Malaltia,
                    on_delete=models.CASCADE,
                    db_column='codi_cie',
                    related_name='diagnostics')

    class Meta:
        managed      = False
        db_table     = 'diagnosticmalaltia'
        unique_together = [('diagnostic', 'malaltia')]

class Supervisio(models.Model):
    dni_supervisor = models.ForeignKey(
                        Metge,
                        on_delete=models.CASCADE,
                        db_column='supervisor_dni',
                        related_name='supervisats',
                        primary_key=True)
    dni_supervisat = models.ForeignKey(
                        Metge,
                        on_delete=models.CASCADE,
                        db_column='supervisat_dni',
                        related_name='supervisors')

    class Meta:
        managed      = False
        db_table     = 'supervisio'
        unique_together = [('dni_supervisor', 'dni_supervisat')]


class CentreMedic(models.Model):
    codi_centre = models.CharField(max_length=15, primary_key=True)
    nom         = models.CharField(max_length=150)
    carrer      = models.CharField(max_length=200, blank=True, null=True)
    codi_postal = models.CharField(max_length=10,  blank=True, null=True)
    ciutat      = models.CharField(max_length=100, blank=True, null=True)
    telefon     = models.CharField(max_length=20,  blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'centremedic'

    def __str__(self):
        return self.nom


class Torn(models.Model):
    codi_torn   = models.CharField(max_length=15, primary_key=True)
    dia_setmana = models.CharField(max_length=20)
    hora_inici  = models.TimeField()
    hora_fi     = models.TimeField()
    data_inici  = models.DateField()
    data_fi     = models.DateField()
    dni_metge   = models.ForeignKey(
                    'Metge', on_delete=models.CASCADE, db_column='dni_metge')
    codi_centre = models.ForeignKey(
                    'CentreMedic', on_delete=models.CASCADE, db_column='codi_centre')

    class Meta:
        managed  = False
        db_table = 'torn'

    def __str__(self):
        dies = {1:'Dl',2:'Dm',3:'Dc',4:'Dj',5:'Dv',6:'Ds',7:'Dg'}
        return f"{dies.get(self.dia_setmana,'?')} {self.hora_inici}-{self.hora_fi}"
