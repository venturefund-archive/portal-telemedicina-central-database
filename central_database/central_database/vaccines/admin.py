from django.contrib import admin

from .models import Vaccine, VaccineAlert, VaccineDose


class VaccineAdmin(admin.ModelAdmin):
    list_display = ("system", "code", "display", "description")
    list_filter = ("system", "description")
    search_fields = ["display", "description", "code"]
    ordering = ["system", "code"]


class VaccineDoseAdmin(admin.ModelAdmin):
    list_display = (
        "vaccine",
        "minimum_recommended_age",
        "maximum_recommended_age",
        "dose_order",
        "booster",
        "gender_recommendation",
    )
    list_filter = (
        "vaccine",
        "minimum_recommended_age",
        "maximum_recommended_age",
        "dose_order",
        "booster",
        "gender_recommendation",
    )
    ordering = ["maximum_recommended_age", "dose_order"]


class VaccineAlertAdmin(admin.ModelAdmin):
    list_display = (
        "vaccine_dose",
        "patient_id",
        "issue",
        "created_at",
        "active",
    )
    list_filter = (
        "vaccine_dose",
        "patient_id",
        "issue",
        "active",
    )
    ordering = ["-created_at"]


admin.site.register(Vaccine, VaccineAdmin)
admin.site.register(VaccineDose, VaccineDoseAdmin)
admin.site.register(VaccineAlert, VaccineAlertAdmin)
