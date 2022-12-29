from django.db import models

from central_database.base_models import CDModel


class Client(CDModel):
    dataset_id = models.CharField(max_length=255)
    fhir_store_id = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)

    def __str__(self):
        return self.client_name
