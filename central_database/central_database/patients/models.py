from django.db import models


class Patient(models.Model):
    """
    Stores **data** from patients.
    """

    UNDEFINED = ""
    MALE = "M"
    FEMALE = "F"
    SEX = ((UNDEFINED, ""), (MALE, "Male"), (FEMALE, "Female"))

    full_name = models.CharField(max_length=200, blank=True, default="")
    social_name = models.CharField(max_length=200, blank=True, default="")
    date_birth = models.DateField(null=True, blank=True, db_index=True)
    sex = models.CharField(
        max_length=1,
        choices=SEX,
        blank=True,
        default=UNDEFINED,
        help_text="M - Male | F - Female",
    )


class Vaccine(models.Model):
    limit_date = models.DateField()
    name_of_vaccine = models.CharField(max_length=200)


class VaccineStatus(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.PROTECT)
    completed = models.BooleanField(default=False)
