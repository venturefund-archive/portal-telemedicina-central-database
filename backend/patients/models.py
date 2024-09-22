from django.db import models
from django.contrib.postgres.fields import ArrayField
from utils.base_models import CDModel


class Address(models.Model):
    line = models.CharField(max_length=1000, blank=True, null=True, help_text="Comma-separated address lines")
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)

    def get_line_list(self):
        return [line.strip() for line in self.line.split(',')] if self.line else []

    def set_line_list(self, line_list):
        self.line = ', '.join(line_list)

    def __str__(self):
        return f"{self.line}, {self.city}, {self.state}, {self.postal_code}, {self.country}"


class Patient(CDModel):
    fhir_id = models.CharField(max_length=255, unique=True)
    given_name = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    family_name = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{' '.join(self.given_name or [])} {self.family_name or ''} ({self.fhir_id})"
    
    def save(self, *args, **kwargs):
        if not self.full_name:
            given = ' '.join(self.given_name) if self.given_name else ''
            family = self.family_name if self.family_name else ''
            self.full_name = f"{given} {family}".strip()
        super().save(*args, **kwargs)

    @property
    def full_address(self):
        address_parts = [
            ', '.join(self.address_line or []),
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ', '.join(filter(None, address_parts))

