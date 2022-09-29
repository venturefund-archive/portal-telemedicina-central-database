from django.contrib import admin
from patients.models import Patient, Vaccine, VaccineStatus

admin.site.register(Patient)
admin.site.register(Vaccine)
admin.site.register(VaccineStatus)
