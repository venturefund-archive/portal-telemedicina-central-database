from django.contrib import admin

from .models import Vaccine, VaccineDose


class VaccineAdmin(admin.ModelAdmin):
    list_display = ("system", "code", "display", "description")
    list_filter = ("system", "code", "display", "description")
    search_fields = ["display", "description"]


class VaccineDoseAdmin(admin.ModelAdmin):
    list_display = (
        "vaccine",
        "minimum_recommended_age",
        "maximum_recommended_age",
        "dose_order",
        "booster",
    )
    list_filter = (
        "vaccine",
        "minimum_recommended_age",
        "maximum_recommended_age",
        "dose_order",
        "booster",
    )
    ordering = ["maximum_recommended_age", "dose_order"]


admin.site.register(Vaccine, VaccineAdmin)
admin.site.register(VaccineDose, VaccineDoseAdmin)
