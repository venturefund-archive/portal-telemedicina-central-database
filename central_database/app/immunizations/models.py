from __future__ import annotations
from datetime import datetime
from unipath import Path
from uuid import uuid4

from django.db import models
from django.core.validators import MinValueValidator

from app.base_models import CDPModel
from app.patients.models import Patient, DataSource
from app.conditions.models import Condition
from app.professionals.models import Profession
from app.medicines.models import Brand
from app.sources.models import Source


def set_directory_and_filename_of_uploaded_file(instance: Immunization, filename: str) -> str:
    extension = filename.split('.')[-1]
    path = Path(filename)
    instance.original_filename = str(path.name)
    date = instance.immunization.date if instance.immunization.date is not None else datetime.now().date()
    return f'immunization_files/{date.year}/{date.month}/{date.day}/{uuid4().hex}.{extension}'


class Vaccine(CDPModel, models.Model):
    '''
    This class is used to represent the Vaccines made by manufacturers.
    '''
    name = models.CharField(max_length=100, help_text='Vaccine name')
    manufacturer = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL, related_name='vaccines')
    number_of_doses = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)], help_text='The recommended number of doses to achieve immunity'
    )
    target_diseases = models.ManyToManyField(
        Condition, related_name='vaccines', help_text='The vaccine preventable diseases'
    )
    data_source = models.ForeignKey(DataSource, on_delete=models.PROTECT, related_name='vaccines', null=True)
    original_id = models.CharField(
        max_length=100, blank=True, default='',
        help_text=(
            'Original ID on Data Source. If the data came from ANVISA website, it\'s the \"register\" field. If the'
            ' data came from a database, it\'s \"Tablename.Primarykeycolumnname.value\"'
        )
    )

    class Meta:
        indexes = [
            models.Index(fields=['name', 'manufacturer']),
            models.Index(fields=['manufacturer', 'name'])
        ]

    def __str__(self):
        return self.name


class Immunization(CDPModel, models.Model):
    '''
    This class is used to represent the event of a patient being administered a vaccine.
    '''
    date = models.DateField(blank=True, null=True, help_text='Date that the immunization occurred.')
    time = models.TimeField(blank=True, null=True, help_text='Time that the immunization occurred.')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='immunizations')
    performer = models.ForeignKey(
        Profession, null=True, on_delete=models.SET_NULL, related_name='immunizations',
        help_text='Indicates who performed the immunization event.'
    )
    location = models.ForeignKey(
        Source, null=True, on_delete=models.SET_NULL, related_name='immunizations',
        help_text='The location where the immunization occurred.'
    )
    vaccine = models.ForeignKey(
        Vaccine, on_delete=models.PROTECT, related_name='immunizations', help_text='The vaccine administered.'
    )
    lot_number = models.CharField(max_length=100, blank=True, help_text='Lot number of the vaccine administered.')
    dose_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)], help_text='Dose number. Example: 1 refers to first dose.'
    )
    original_id = models.CharField(
        max_length=100, blank=True, default='',
        help_text='Original ID on Data Source. Recommended format: \"Tablename.Primarykeycolumnname.value\"'
    )

    class Meta:
        indexes = [
            models.Index(fields=['patient', 'date', 'vaccine']),
            models.Index(fields=['patient', 'vaccine', 'date']),
            models.Index(fields=['vaccine', 'patient', 'date']),
            models.Index(fields=['vaccine', 'date', 'patient']),
            models.Index(fields=['date', 'vaccine', 'patient']),
            models.Index(fields=['date', 'patient', 'vaccine']),
        ]

    def __str__(self):
        return f'Immunization of patient [{self.patient}] by the vaccine [{self.vaccine}]'


class ImmunizationFile(CDPModel, models.Model):
    '''
    This class is used to represent the files associated in an immunization.
    '''
    immunization = models.ForeignKey(Immunization, on_delete=models.CASCADE, related_name='immunization_files')
    archive = models.FileField(
        max_length=500, upload_to=set_directory_and_filename_of_uploaded_file, help_text='File content'
    )
    original_id = models.CharField(
        max_length=100, blank=True, default='',
        help_text=('Original ID on Data Source. Recommended format: \"Tablename.Primarykeycolumnname.value\"')
    )
    original_filename = models.CharField(max_length=500, blank=True, help_text='Original file location: url, path')

    def __str__(self):
        return self.original_filename

    @property
    def extension(self):
        return self.original_filename.split('.')[-1]
