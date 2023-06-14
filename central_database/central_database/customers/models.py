from django.contrib.gis.db import models as gis_models
from django.db import models

from central_database.base_models import CDModel


class Client(CDModel):
    dataset_id = models.CharField(max_length=255)
    fhir_store_id = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, default="test_city", null=True)

    def __str__(self):
        return self.client_name


class HealthProfessional(CDModel):
    name = models.CharField(max_length=255)
    cns_number = models.CharField(max_length=32)
    cnes_number = models.CharField(max_length=16, null=True, blank=True)
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, null=True, blank=True
    )  # noqa: E501

    class Meta:
        indexes = [models.Index(fields=["cns_number"])]

    def __str__(self):
        return f"{self.cns_number} : {self.name}"


class MicroRegion(gis_models.Model):
    name = gis_models.CharField(max_length=255)
    polygon = gis_models.PolygonField()
    client = gis_models.ForeignKey(
        Client, related_name="micro_regions", on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name

    @staticmethod
    def get_for_client(client):
        return MicroRegion.objects.filter(client=client)
