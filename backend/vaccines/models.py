from django.db import models
from django.utils import timezone
from utils.base_models import CDModel
from customers.models import FhirStore, HealthProfessional, Client
from users.models import User


class Vaccine(CDModel, models.Model):
    system = models.CharField(max_length=255, help_text="Coding system for the vaccine code")
    code = models.CharField(max_length=50, help_text="Vaccine code")
    display = models.CharField(max_length=255, help_text="Display name for the vaccine")
    description = models.TextField(null=True, blank=True, help_text="Description of the vaccine")

    class Meta:
        unique_together = ['system', 'code']

    def __str__(self):
        return f"{self.system}: {self.code} - {self.display}"


class VaccineDose(CDModel, models.Model):
    GENDER_CHOICES = [
        ('B', 'Both'),
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name="doses")
    minimum_recommended_age = models.PositiveIntegerField(null=True, blank=True, help_text="Minimum recommended age in months")
    maximum_recommended_age = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum recommended age in months")
    dose_order = models.PositiveSmallIntegerField(help_text="The order of this dose in the vaccination schedule")
    booster = models.BooleanField(default=False, null=True, blank=True, help_text="Whether this is a booster dose")
    gender_recommendation = models.CharField(max_length=1, choices=GENDER_CHOICES, default='B')

    class Meta:
        unique_together = ['vaccine', 'dose_order', 'gender_recommendation']

    def __str__(self):
        return f"{self.vaccine.display} - Dose {self.dose_order}"


class Immunization(CDModel, models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('entered-in-error', 'Entered in Error'),
        ('not-done', 'Not Done'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    occurrence_date = models.DateField() 
    primary_source = models.BooleanField(default=True)
    performer = models.ForeignKey(HealthProfessional, on_delete=models.PROTECT, null=True, blank=True)
    recommendation = models.ForeignKey('ImmunizationRecommendation', on_delete=models.SET_NULL, null=True, blank=True, related_name='immunizations')

    def __str__(self):
        return f"Immunization for patient {self.patient_id}: {self.vaccine_dose}"
    
    def is_completed(self):
        return self.status == 'completed'

    def is_not_done(self):
        return self.status == 'not-done'

    def get_application_date(self):
        return self.occurrence_date if self.is_completed() else None
    
    def update_recommendation(self):
        if self.recommendation:
            if self.status == 'completed':
                self.recommendation.forecast_status = 'complete'
            elif self.status == 'not-done':
                self.recommendation.forecast_status = 'overdue'
            self.recommendation.save()

    @classmethod
    def get_patient_immunizations(cls, patient_id):
        return cls.objects.filter(recommendation__patient_id=patient_id)


class ImmunizationRecommendation(CDModel, models.Model):
    FORECAST_STATUS_CHOICES = [
        ('due', 'Due'),
        ('overdue', 'Overdue'),
        ('immune', 'Immune'),
        ('contraindicated', 'Contraindicated'),
        ('complete', 'Complete'),
    ]

    patient_id = models.CharField(max_length=255, help_text="Patient ID from FHIR")
    date = models.DateField(null=True, blank=True)
    vaccine_dose = models.ForeignKey(VaccineDose, on_delete=models.PROTECT)
    forecast_status = models.CharField(max_length=20, choices=FORECAST_STATUS_CHOICES, null=True, blank=True)
    forecast_reason = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    fhir_store = models.ForeignKey(FhirStore, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"Immunization Recommendation for patient {self.patient_id}: {self.vaccine_dose}"
    
    def is_due(self):
        return self.forecast_status == 'due'

    def is_overdue(self):
        return self.forecast_status == 'overdue'

    def is_completed(self):
        return self.forecast_status == 'complete'

    def get_alert_status(self):
        if self.is_overdue():
            return 'alert'
        elif self.is_due():
            return 'due'
        elif self.is_completed():
            return 'completed'
        else:
            return 'normal'
        
    def silence_alert(self, user, reason=''):
        
        immunization = Immunization.objects.create(
            status='not-done',
            occurrence_date=timezone.now(),
            primary_source=True,
            recommendation=self,
            patient_id=self.patient_id
        )
        
        ImmunizationAlertSilence.objects.create(
            immunization=immunization,
            silenced_by=user,
            reason=reason
        )
        
        self.forecast_status = 'complete'
        self.save()
        
        return immunization

    @classmethod
    def get_patient_recommendations(cls, patient_id):
        return cls.objects.filter(patient_id=patient_id)


class ImmunizationAlertSilence(CDModel, models.Model):
    immunization = models.ForeignKey(Immunization, on_delete=models.CASCADE)
    silenced_at = models.DateTimeField(auto_now_add=True)
    silenced_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reason = models.TextField(blank=True)

    def __str__(self):
        return f"Alert silence for {self.immunization_recommendation}"


class VaccineProtocol(CDModel, models.Model):
    name = models.CharField(max_length=255, help_text="Protocol Name")
    description = models.CharField(max_length=100)
    vaccine_doses = models.ManyToManyField(VaccineDose)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"Vaccine Protocol: {self.name}"


class VaccinationCard(CDModel):
    patient_id = models.CharField(max_length=255, help_text="Patient ID from FHIR")
    document = models.FileField(upload_to="vaccination_cards/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Vaccination Card for patient {self.patient_id}"
