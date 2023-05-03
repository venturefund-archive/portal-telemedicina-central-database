from django.db import models


class PatientProxy(models.Model):
    """
    Proxy model for Patient FHIR resource.
    This model is used only for creating ContentType and Permission objects.
    """

    class Meta:
        managed = False
        permissions = [
            ("view_patient", "Can view patient"),
            ("add_patient", "Can add patient"),
            ("change_patient", "Can change patient"),
            ("delete_patient", "Can delete patient"),
        ]
