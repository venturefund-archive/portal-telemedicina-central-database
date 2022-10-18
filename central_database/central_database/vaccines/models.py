from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models

from central_database.base_models import Alert, CDModel


class Vaccine(CDModel, models.Model):
    """
    This class is used to represent the Vaccines registered
    by different value sets.
    """

    CVX = "CVX"
    BRI = "BRI"
    SYSTEM_VALUE_SETS = [
        (CVX, "http://hl7.org/fhir/sid/cvx"),
        (
            BRI,
            "https://integracao.esusab.ufsc.br/ledi/documentacao/referencias/dicionario.html#imunobiologico",  # noqa: E501
        ),
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
        max_length=200,
        help_text="Small text description from display field on FHIR.",  # noqa: E501
    )
    description = models.CharField(
        max_length=200, help_text="Full text description of the vaccine."
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


class VaccineDose(CDModel, models.Model):
    """
    This class is used to represent the Vaccine Doses recommended
    for certain ages.
    """

    MALE = "M"
    FEMALE = "F"
    BOTH = "B"
    GENDER_RECOMMENDATION = [
        (BOTH, "Both"),
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]  # noqa: E501

    vaccine = models.ForeignKey(
        Vaccine, on_delete=models.CASCADE, related_name="vaccines"
    )
    minimum_recommended_age = models.PositiveIntegerField(
        help_text="The minimum age, in months, if the administration can be performed within a range. If there is no range, leave it blank and use only the maximum recommended age.",  # noqa: E501
        blank=True,
        null=True,
        default=None,
    )
    maximum_recommended_age = models.PositiveIntegerField(
        help_text="The maximum age, in months, if the administration can be performed within a range. If there is no range, this is the recommended age."  # noqa: E501
    )
    dose_order = models.PositiveSmallIntegerField(
        help_text="The order of this dose in the vaccination schedule."
    )
    booster = models.BooleanField(
        help_text="Check if this is considered a booster shot in the vaccination schedule."  # noqa: E501
    )

    gender_recommendation = models.CharField(
        max_length=1,
        choices=GENDER_RECOMMENDATION,
        default="B",
        help_text="Select if this dose is gender specific.",
    )

    class Meta:
        indexes = [
            models.Index(fields=["vaccine"]),
            models.Index(fields=["maximum_recommended_age"]),
        ]

        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    maximum_recommended_age__gt=models.F(
                        "minimum_recommended_age"
                    )  # noqa: E501
                ),
                name="age_max_greater_age_min",
            ),
            models.UniqueConstraint(
                fields=["vaccine", "dose_order", "gender_recommendation"],
                name="unique_vaccine_dose_order_gender_recommendation",  # noqa: E501
            ),
        ]

    def clean(self, *args, **kwargs):
        prior_dose = VaccineDose.objects.filter(
            vaccine=self.vaccine,
            dose_order__lt=self.dose_order,
            gender_recommendation=self.gender_recommendation,
        ).first()
        next_dose = VaccineDose.objects.filter(
            vaccine=self.vaccine,
            dose_order__gt=self.dose_order,
            gender_recommendation=self.gender_recommendation,
        ).first()

        if prior_dose:
            if (
                self.maximum_recommended_age
                < prior_dose.maximum_recommended_age  # noqa: E501
            ):  # noqa: E501
                raise ValidationError(
                    "Max recommended age for a dose must be greater than the max recommended age from a prior dose."  # noqa: E501
                )
        if next_dose:
            if (
                self.maximum_recommended_age
                > next_dose.maximum_recommended_age  # noqa: E501
            ):  # noqa: E501
                raise ValidationError(
                    "Max recommended age for a dose must be less than the max recommended age from a subsequent dose."  # noqa: E501
                )

        super().clean(*args, **kwargs)

    def __str__(self):
        return f"Vaccine: {self.vaccine} - Dose: {self.dose_order}"


class VaccineAlert(Alert, models.Model):
    """
    This class is used to represent a Vaccine alert.
    """

    DELAY = "Delayed"
    VACCINATION_ISSUES = [
        (DELAY, "Dose is delayed"),
    ]

    vaccine_dose = models.ForeignKey(
        VaccineDose, on_delete=models.CASCADE, related_name="vaccine_doses"
    )
    patient_id = models.PositiveIntegerField(help_text="Patient ID from FHIR.")
    issue = models.CharField(
        max_length=50,
        choices=VACCINATION_ISSUES,
        help_text="Vaccination issue communicated by this alert.",
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    active = models.BooleanField(
        default=True, help_text="Check if this alert is active."
    )

    class Meta:
        indexes = [
            models.Index(fields=["patient_id"]),
            models.Index(fields=["issue"]),
            models.Index(fields=["created_at"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["vaccine_dose", "patient_id", "issue"],
                name="unique_dose_alert_type_per_patient",
            )
        ]

    def __str__(self):
        return f"Vaccine dose {self.vaccine_dose} for patient {self.patient_id} is {self.issue}."  # noqa: E501
