from django.db import models

from central_database.base_models import CDModel


class Client(CDModel):
    dataset_id = models.CharField(max_length=255)
    fhir_store_id = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)

    PREFECTURE = "Prefecture"
    CLIENT_TYPE = [
        (PREFECTURE, "Prefecture"),
    ]  # noqa: E501

    client_type = models.CharField(
        max_length=255,
        choices=CLIENT_TYPE,
        help_text="Select the type of client ",
        default="Prefecture",
    )

    ibge_population = models.IntegerField(null=True, blank=True)
    children_born_alive = models.IntegerField(null=True, blank=True)
    children_registered_in_APS = models.IntegerField(null=True, blank=True)
    sisab_municipal_registration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.client_name
