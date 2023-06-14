from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Client, MicroRegion


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("dataset_id", "fhir_store_id", "client_name")


@admin.register(MicroRegion)
class MicroRegionAdmin(LeafletGeoAdmin):
    pass
