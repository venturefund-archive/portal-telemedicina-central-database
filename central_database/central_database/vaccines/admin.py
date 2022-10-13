from django.contrib import admin

from .models import Vaccine


class VaccineAdmin(admin.ModelAdmin):
    list_display = ("system", "code", "display", "description")
    list_filter = ("system", "code", "display", "description")


admin.site.register(Vaccine, VaccineAdmin)
