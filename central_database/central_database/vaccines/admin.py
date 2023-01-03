from django.contrib import admin

from .models import (  # noqa
    Vaccine,
    VaccineAlert,
    VaccineAlertType,
    VaccineDose,
    VaccineStatus,
)


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ("system", "code", "display", "description")
    list_filter = ("system", "description")
    search_fields = ["display", "description", "code"]
    ordering = ["system", "code"]


@admin.register(VaccineDose)
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


@admin.register(VaccineAlertType)
class VaccineAlertTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "description_pt_br")
    list_filter = ("id", "description", "description_pt_br")
    search_fields = ["description"]
    ordering = ["id"]


@admin.register(VaccineAlert)
class VaccineAlertAdmin(admin.ModelAdmin):
    list_display = (
        "vaccine_dose",
        "patient_id",
        "alert_type",
        "created_at",
        "active",
    )
    list_filter = (
        "vaccine_dose",
        "patient_id",
        "alert_type",
        "active",
    )
    ordering = ["-created_at"]


@admin.register(VaccineStatus)
class VaccineStatusAdmin(admin.ModelAdmin):
    list_display = ("vaccine_dose", "patient_id", "completed")
    list_filter = ("vaccine_dose", "patient_id", "completed")
    ordering = ["id"]
