from collections import defaultdict
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models

from central_database.base_models import Alert, AlertType, CDModel


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

    def get_vaccine_alerts(self, patient_id):
        return VaccineAlert.objects.filter(
            vaccine_dose=self.id, active=True, patient_id=patient_id
        )

    def get_vaccine_status(self, patient_id):
        return VaccineStatus.objects.filter(
            vaccine_dose=self.id, patient_id=patient_id
        )  # noqa: E501

    def alerts_count(self):
        return self.vaccine_alerts.count()

    @staticmethod
    def get_alerts_count_by_dose(dose_id):
        return VaccineDose.objects.get(id=dose_id).alerts_count()


class VaccineAlertType(AlertType, models.Model):
    """
    This class is used to represent a type of alert for Vaccines.
    """

    description = models.CharField(
        max_length=100,
        help_text="Describe the event/issue this alert is representing.",  # noqa: E501
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["description"], name="unique_description"
            ),  # noqa: E501
            models.UniqueConstraint(
                fields=["description_pt_br"], name="unique_description_pt_br"
            ),
        ]

    def __str__(self):
        return f"{self.id}: {self.description}"


class VaccineStatus(CDModel, models.Model):
    vaccine_dose = models.ForeignKey(
        VaccineDose, on_delete=models.CASCADE
    )  # noqa: E501
    patient_id = models.CharField(
        max_length=255, help_text="Patient ID from FHIR."
    )  # noqa: E501
    completed = models.BooleanField(default=False)

    application_date = models.DateField(blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=["patient_id"])]  # noqa: E501

    def __str__(self):
        return f"Vaccine dose {self.vaccine_dose} for patient {self.patient_id} has completion status: {self.completed}."  # noqa: E501

    @staticmethod
    def get_completed_count_by_dose(dose):
        return VaccineStatus.objects.filter(
            vaccine_dose=dose, completed=True
        ).count()  # noqa: E501


class VaccineAlert(Alert, models.Model):
    """
    This class is used to represent a Vaccine alert.
    """

    vaccine_dose = models.ForeignKey(
        VaccineDose, related_name="vaccine_alerts", on_delete=models.CASCADE
    )
    patient_id = models.CharField(
        max_length=255, help_text="Patient ID from FHIR."
    )  # noqa: E501
    alert_type = models.ForeignKey(
        VaccineAlertType,
        on_delete=models.CASCADE,
        related_name="vaccine_alert_types",  # noqa: E501
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    active = models.BooleanField(
        default=True, help_text="Check if this alert is active."
    )

    class Meta:
        indexes = [
            models.Index(fields=["patient_id", "vaccine_dose"]),
            models.Index(fields=["alert_type"]),
            models.Index(fields=["created_at"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["vaccine_dose", "patient_id", "alert_type"],
                name="unique_dose_alert_type_per_patient",
            )
        ]

    def clean(self, *args, **kwargs):
        vaccine_dose_status = VaccineStatus.objects.filter(  # noqa
            patient_id=self.patient_id, vaccine_dose=self.vaccine_dose  # noqa
        )
        if (
            vaccine_dose_status.exists()
            and vaccine_dose_status.first().completed  # noqa
        ):  # noqa: E501
            raise ValidationError(
                "It's not possible to create an vaccine dose alert to this patient, since it's already completed."  # noqa: E501
            )

        super().clean(*args, **kwargs)

    def __str__(self):
        return f"Vaccine dose {self.vaccine_dose} for patient {self.patient_id} has alert: {self.alert_type}."  # noqa: E501

    @staticmethod
    def get_number_of_alerts_by_patient(patient_id, vaccine_dose):
        return VaccineAlert.objects.filter(
            patient_id=patient_id, vaccine_dose=vaccine_dose, active=True
        ).count()

    @staticmethod
    def get_alerts_by_doses(vaccine_doses):
        return VaccineAlert.objects.filter(vaccine_dose__in=vaccine_doses)

    @staticmethod
    def get_alerts_by_patient(patient_ids):
        alerts = (
            VaccineAlert.objects.filter(patient_id__in=patient_ids)
            .select_related("vaccine_dose__vaccine")
            .values("patient_id", "vaccine_dose__vaccine__display")
        )

        alerts_dict = defaultdict(list)
        for alert in alerts:
            alerts_dict[alert["patient_id"]].append(
                alert["vaccine_dose__vaccine__display"]
            )

        return dict(alerts_dict)


class VaccineProtocol(models.Model):
    vaccine_doses = models.ManyToManyField(VaccineDose)
    name = models.CharField(max_length=255, help_text="Protocol Name")
    description = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"Vaccine Protocol: {self.name}"

    @staticmethod
    def get_vaccine_protocol_by_client(client_id=None):
        if not client_id:
            return VaccineProtocol.objects.prefetch_related(
                "vaccine_doses__vaccine_alerts"
            ).first()

    def get_number_of_doses_with_alerts_by_patient(self):
        vaccine_doses = self.vaccine_doses.all().values_list("id", flat=True)

        alerts = (
            VaccineAlert.get_alerts_by_doses(vaccine_doses)
            .values("patient_id")
            .annotate(number_of_alerts=models.Count("patient_id"))
        )
        alerts_dict = {
            item["patient_id"]: item["number_of_alerts"] for item in alerts
        }  # noqa: E501
        return alerts_dict

    def get_total_amount_of_completed_doses(self):
        return VaccineStatus.objects.filter(
            vaccine_dose__in=self.vaccine_doses.all(), completed=True
        ).count()

    def get_total_amount_of_alert_doses(self):
        return VaccineAlert.objects.filter(
            vaccine_dose__in=self.vaccine_doses.all()
        ).count()
