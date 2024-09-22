from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Client, Dataset, FhirStore, MicroRegion


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    pass


@admin.register(FhirStore)
class FhirStoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("fhir_store", "client_name")


@admin.register(MicroRegion)
class MicroRegionAdmin(LeafletGeoAdmin):
    pass
