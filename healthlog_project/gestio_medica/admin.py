from django.contrib import admin
from .models import Persona, Metge, Pacient, Tractament, Medicament, Prescripcio

admin.site.register(Metge)
admin.site.register(Pacient)
admin.site.register(Tractament)
admin.site.register(Medicament)
admin.site.register(Prescripcio)