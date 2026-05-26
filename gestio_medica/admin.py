from django.contrib import admin

# Register your models here.
from .models import Pacient, Metge, Prescripcio, Medicament, Tractament 

# Los registramos uno a uno
admin.site.register(Pacient)
admin.site.register(Metge)
admin.site.register(Prescripcio)
admin.site.register(Tractament)
admin.site.register(Medicament)