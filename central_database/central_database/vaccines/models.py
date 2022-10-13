from django.db import models

from central_database.base_models import CDModel


class Vaccine(CDModel, models.Model):
    """
    This class is used to represent the Vaccines registered
    by different value sets.
    """

    CVX = "CVX"
    BRI = "BRI"
    SYSTEM_VALUE_SETS = [
        (CVX, "http://hl7.org/fhir/sid/cvx"),
        (BRI, "http://www.saude.gov.br/fhir/r4/CodeSystem/BRImunobiologico"),
    ]
    system = models.CharField(
        max_length=3,
        choices=SYSTEM_VALUE_SETS,
        help_text="Which system of codes is used on FHIR to define the vaccine codes.",  # noqa: E501
    )
    code = models.PositiveSmallIntegerField(
        help_text="Vaccine code used defined on a specific system."
    )
    display = models.CharField(
        max_length=100,
        help_text="Small text description from display field on FHIR.",  # noqa: E501
    )
    description = models.CharField(
        max_length=100, help_text="Full text description of the vaccine."
    )

    class Meta:
        indexes = [
            models.Index(fields=["system", "code"]),
            models.Index(fields=["code", "system"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["system", "code"], name="unique_system_code"
            )
        ]

    def __str__(self):
        return f"{self.system}: {self.code} - {self.display}"
