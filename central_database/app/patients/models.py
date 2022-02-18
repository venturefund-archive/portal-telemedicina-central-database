import datetime
import re
import googlemaps
import requests
import json
import pytz
import logging

from dateutil.relativedelta import relativedelta

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.apps import apps
from django.utils import timezone
from django.conf import settings

from app.base_models import CDPModel, ReplicableCDPModel
from app.empi import EMPI

from .querysets import AddressManager, ContactManager, DocumentManager, PatientManager

logger = logging.getLogger('logger')


class DataSource(CDPModel, models.Model):
    '''
    Source where data come from. Ex: Portal, MEDEX, etc.
    '''
    NO_AUTH = ''
    BASIC = 'Basic'
    TOKEN = 'Token'
    OAUTH_2 = 'Bearer'
    CUSTOM = 'Custom'
    AUTH_TYPES = (
        (NO_AUTH, ''),
        (BASIC, 'Basic Authentication'),
        (TOKEN, 'Token Based Authentication'),
        (OAUTH_2, 'OAUTH2 Authentication'),
        (CUSTOM, 'Custom Authentication'),
    )

    identifier = models.SlugField(max_length=50, unique=True)
    description = models.CharField(max_length=2000)
    system_identifier = models.CharField(max_length=64, blank=True)
    ldp_host = models.CharField(max_length=150, blank=True)
    general_endpoint = models.CharField(max_length=150, blank=True)
    empi_endpoint = models.CharField(max_length=150, blank=True)
    severity_endpoint = models.CharField(max_length=150, blank=True)
    structured_report_endpoint = models.CharField(max_length=150, blank=True)
    auth_type = models.CharField(max_length=6, choices=AUTH_TYPES, default=NO_AUTH, blank=True)
    auth_endpoint = models.CharField(max_length=150, blank=True)
    auth_request = models.TextField(max_length=2000, blank=True)
    auth_token_key = models.CharField(max_length=50, default='token', blank=True)
    auth_expiration_key = models.CharField(max_length=50, default='expires', blank=True)
    auth_response_header = models.TextField(max_length=2000, blank=True)
    token = models.CharField(max_length=400, blank=True)
    token_expiration = models.DateTimeField(blank=True, null=True)
    allow_require_severity = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'data sources'
        ordering = ['identifier']
        indexes = [
            models.Index(fields=['identifier']),
        ]

    def third_party_authentication(self):

        def sub_key(data, key_list):
            aux = data
            for key in key_list.split('|'):
                if key in aux:
                    aux = aux[key]
                else:
                    logger.error(f'Invalid auth key: {key}.')
                    return ''
            return aux

        def headers():
            headers = {
                'Content-Type': 'application/json'
            }
            if self.auth_type == self.OAUTH_2:
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
            return headers

        if self.auth_endpoint != '' and self.auth_type != DataSource.NO_AUTH:
            if self.token_expiration is None or self.token_expiration <= timezone.make_aware(datetime.datetime.now()):
                res = requests.post(
                    self.auth_endpoint,
                    data=self.auth_request,
                    headers=headers()
                )
                if res.status_code != 200:
                    logger.error(f'Failed to authenticate to: {self.auth_endpoint}.')
                    logger.error(f'Request body was {self.auth_request}.')
                    logger.error(f'Response status code was {res.status_code}.')
                    logger.error(f'Response body was {res.content}.')
                    return {}
                data = None
                try:
                    data = res.json()
                except Exception:
                    logger.error(f'Response body was not JSON serializable: {res.content}.')
                if data is not None:
                    self.token = sub_key(data, self.auth_token_key)
                    exp_dt = sub_key(data, self.auth_expiration_key)
                    dt_format = '%Y-%m-%dT%H:%M:%S'
                    if isinstance(exp_dt, int):
                        aux_date = timezone.make_aware(
                            datetime.datetime.now(),
                            pytz.timezone('UTC')
                         ) + datetime.timedelta(seconds=exp_dt)
                        exp_dt = aux_date.strftime(dt_format)
                    exp_dt = exp_dt.split('.')[0] if '.' in exp_dt else exp_dt
                    if 'T' not in exp_dt:
                        dt_format = dt_format.replace('T', ' ')
                    self.token_expiration = timezone.make_aware(
                        datetime.datetime.strptime(exp_dt, dt_format),
                        pytz.timezone('UTC')
                    )
                    self.save()
            if self.auth_type == self.CUSTOM:
                custom_header = (
                    self.auth_response_header
                    .replace('{$AUTH_TYPE}', self.auth_type)
                    .replace('{$TOKEN}', self.token)
                )
                return json.loads(custom_header)
            else:
                return {
                    'Authorization': str(self.auth_type + ' ' + self.token)
                }
        else:
            return {}

    def __str__(self):
        return self.identifier


class Country(CDPModel, models.Model):
    '''
    Countries of the world.
    '''
    name = models.CharField(max_length=100, unique=True)
    acronym = models.CharField(max_length=5, unique=True)

    class Meta:
        verbose_name_plural = 'countries'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['acronym']),
        ]

    def __str__(self):
        return self.name


class State(CDPModel, models.Model):
    '''
    States/Counties of the country.
    '''
    country = models.ForeignKey(Country, related_name='states', on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=5)

    class Meta:
        ordering = ['name', 'id']
        constraints = [
            models.UniqueConstraint(fields=['country', 'acronym'], name='unique_state')
        ]
        indexes = [
            models.Index(fields=['country', 'name']),
            models.Index(fields=['country', 'acronym']),
            models.Index(fields=['name']),
            models.Index(fields=['acronym']),
        ]

    def __str__(self):
        return '{} ({}), {}'.format(self.name, self.acronym, self.country.name)


class City(CDPModel, models.Model):
    '''
    Cities of the state/county.
    '''
    state = models.ForeignKey(State, related_name='cities', on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True, help_text='Latitude geographical coordinate')
    longitude = models.FloatField(blank=True, null=True, help_text='Longitude geographical coordinate')

    class Meta:
        verbose_name_plural = 'cities'
        ordering = ['name', 'id']
        constraints = [
            models.UniqueConstraint(fields=['state', 'name'], name='unique_city')
        ]
        indexes = [
            models.Index(fields=['state', 'name']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return '{} - {}'.format(self.name, self.state.acronym)

    def save(self, *args, **kwargs):
        super(City, self).save(*args, **kwargs)
        if (self.latitude is None or self.longitude is None) and settings.CITY_GEOCODING_ENABLED:
            publisher = self.connect_to_pubsub()
            topic = f'{settings.TOPICS_FOLDER}{settings.PUBSUB_ENVIRONMENT}_city_geocode'
            data = {
                'id': self.id
            }
            data = json.dumps(data).encode('utf-8')
            future = publisher.publish(topic, data)
            ex = future.exception()
            if ex is None:
                logger.info('Sending a city to geolocate')
                logger.debug(f'Topic: {topic}')
                logger.debug(f'Payload: {data}')
            else:
                logger.error(ex)

    def complete_description(self):
        return '{} - {}, {}'.format(self.name, self.state.acronym, self.state.country.name)

    def geocode(self):
        ''' Get latitude and longitude of a new city from Google Maps'''
        gmaps = googlemaps.Client(key=settings.GOOGLE_GEOCODE_API_KEY)
        geocode_result = gmaps.geocode(self.complete_description())
        if geocode_result is not None:
            city = geocode_result[0]
            if city is not None:
                if 'partial_match' not in city or not city['partial_match']:
                    geocode = city['geometry']['location']
                    self.latitude = geocode['lat']
                    self.longitude = geocode['lng']
        return geocode_result


class Patient(CDPModel, models.Model):
    '''
    Stores **data** from patients.
    '''
    UNDEFINED = ''
    MALE = 'M'
    FEMALE = 'F'
    SEX = (
        (UNDEFINED, ''),
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )
    UNRATED = ''
    SUSPECT = 'S'
    CLEAR = 'C'
    SUSPECT_STATUS = (
        (UNRATED, 'Unrated'),
        (SUSPECT, 'Suspect'),
        (CLEAR, 'Clear')
    )
    NOT_INFORMED = ''
    AUTOMATIC = 'A'
    MANUAL = 'M'
    EMPI_TYPES = (
        (NOT_INFORMED, 'Not informed'),
        (AUTOMATIC, 'Automatic'),
        (MANUAL, 'Manual')
    )

    master_patient = models.ForeignKey(
        'self', related_name='original_patients', on_delete=models.SET_NULL, null=True, blank=True
    )
    data_source = models.ForeignKey(
        DataSource, related_name='patients', on_delete=models.PROTECT, null=True, blank=True
    )
    original_id = models.CharField(
        max_length=100, blank=True, default='',
        help_text=('Original ID on Data Source. Recommended format: \"Tablename.Primarykeycolumnname.value\"')
    )
    unique_id = models.SlugField(blank=True, default='', db_index=True, help_text='Master Patient Index')
    full_name = models.CharField(max_length=200, blank=True, default='', db_index=True)
    social_name = models.CharField(max_length=200, blank=True, default='')
    date_birth = models.DateField(null=True, blank=True, db_index=True)
    date_death = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX, blank=True, default=UNDEFINED, help_text='M - Male | F - Female')
    viewed = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=SUSPECT_STATUS, blank=True, default=UNRATED)
    empi_type = models.CharField(
        max_length=1, choices=EMPI_TYPES, blank=True, default=NOT_INFORMED,
        help_text='If the patient was analized by a human or robot in the EMPI'
    )

    objects = PatientManager()

    @property
    def is_master_patient(self):
        '''Checks if the patient is the master patient.'''
        return self.data_source is None and self.unique_id != ''

    @property
    def lawyers(self):
        Profession = apps.get_model('professionals', 'Profession')
        ret = Profession.objects.none()
        for op in self.original_patients.all() if self.is_master_patient else [self]:
            ret |= Profession.objects.filter(
                lawsuits_as_lawyer__id__in=op.lawsuits.values_list('id', flat=True)
            ).distinct()
        return ret.distinct()

    @property
    def prescribers(self):
        Profession = apps.get_model('professionals', 'Profession')
        ids_list = self.original_patients.all().values_list('id', flat=True) if self.is_master_patient else [self.id]
        return Profession.objects.filter(
            prescriptions__patient__id__in=ids_list
        ).distinct()

    class Meta:
        ordering = ['data_source__id', 'full_name']
        indexes = [
            models.Index(fields=['data_source', 'full_name']),
            models.Index(fields=['data_source', 'original_id']),
            models.Index(fields=['data_source', 'unique_id']),
            models.Index(fields=['sex', 'full_name']),
        ]

    def __str__(self):
        return self.full_name + ((' [' + self.data_source.identifier + ']') if self.data_source is not None else '')

    def clean(self, *args, **kwargs):
        if Patient.objects.filter(
            data_source=self.data_source,
            data_source__isnull=False,
            original_id=self.original_id
        ).exclude(id=self.id).exists():
            raise ValidationError(
                f'Patient with Data Source {self.data_source.identifier} and '
                f'original id {self.original_id} already exists.'
            )
        super(Patient, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):

        old_patient = Patient.objects.filter(id=self.id).first()

        if self.unique_id == '' and self.data_source is not None:
            self.master_patient = None

        if self.unique_id != '' and not self.is_master_patient and self.empi_type == Patient.NOT_INFORMED:
            self.empi_type = Patient.MANUAL

        # Removes orphan Master Patients
        if old_patient is not None and old_patient.unique_id != '' and self.unique_id == '':
            mp = old_patient.master_patient
            # If it have only one OP (it is itself)
            if mp is not None and mp.original_patients.all().count() == 1:
                mp.delete()

        super(Patient, self).save(*args, **kwargs)

        if not self.is_master_patient:
            mp = self.dedup()
            if self.unique_id != '':
                (
                    Patient.objects
                    .filter(data_source__isnull=False, unique_id=self.unique_id)
                    .exclude(master_patient=mp)
                    .update(master_patient=mp)
                )

        if self.unique_id == '':
            self.run_empi(self)

        if self.is_master_patient or settings.CDP_HOST != '':
            from .serializers import PatientSerializer
            up = self.upload_to_cdp(PatientSerializer, model_name='Master Patient')
            if settings.CDP_HOST != '':
                return up

    def upload_data(self, data):
        super(Patient, self).upload_data(data)
        data['data_source'] = settings.LDP_DATASOURCE
        del data['master_patient']
        return data

    def get_mother(self):
        ''' Get patient's mother, which can be more than one if this is a master patient.'''
        return Parent.objects.filter(patient=self, parent_type=Parent.MOTHER)

    def get_father(self):
        ''' Get patient's father, which can be more than one if this is a master patient.'''
        return Parent.objects.filter(patient=self, parent_type=Parent.FATHER)

    def filter_master_patient(self):
        '''Return the Master Patient of the patient.

        Args:
            <none>

        Returns:
            The Master Patient
        '''
        return Patient.objects.filter(unique_id=self.unique_id, data_source__isnull=True).first()

    def dedup(self):
        '''Dedup data from patient into the patient with same unique_id and data_source = None.

        Args:
            <none>

        Returns:
            <none>
        '''
        def informed(v, niv):
            return (v != '') if isinstance(niv, str) else (v is not None)

        def assign_field(field):
            # Assign most voted Data Source Patient's field to Master Patient
            value = getattr(self, field)
            niv = '' if isinstance(value, str) else None  # Not informed value
            count_values = list_patients.values(field).annotate(Count(field)).order_by('-' + field + '__count')
            total = 0 if not informed(value, niv) else 1
            bigger = niv
            longer = niv
            for val in count_values:
                if informed(val[field], niv):
                    total += val[field + '__count'] if informed(val[field], niv) else 0
                    bigger = val if not informed(bigger, niv) else bigger
                    if field == 'full_name' and len(val[field]) > len(longer):
                        longer = val[field]
            max_votes = ((total // 2) + 1) if total > 0 else 0
            voters = list_patients.filter(**{field: value}).count() + 1
            if informed(value, niv) and voters >= max_votes:
                setattr(mp, field, value)
            else:
                if informed(bigger, niv) and bigger[field + '__count'] >= max_votes:
                    setattr(mp, field, bigger[field])
                else:
                    setattr(mp, field, niv)
            # Ensures MP has the full_name filled out
            if field == 'full_name' and mp.full_name == '':
                mp.full_name = longer

        # Dedup only if the current Patient is not the Master Patient itself and has an unique ID pointing to his MP
        mp = None
        if not self.is_master_patient and self.unique_id != '':
            logger.info('Starting patient deduplication.')
            # Get MP or create one
            mp = self.filter_master_patient()
            if mp is None:
                mp = Patient()
                mp.unique_id = self.unique_id
                logger.info('Create new Master Patient.')

            # Dedup Fields and assign to the newly created MP
            list_patients = mp.original_patients.all().exclude(id=self.id)
            exclude_fields = ['id', 'unique_id', 'data_source', 'master_patient', 'empi_type', 'original_id']
            for field in [f.name for f in self._meta.local_fields]:
                if field not in exclude_fields:
                    assign_field(field)
            mp.save()

            # Copy original patients' childrens (like documents, contacts, etc.) to the MP
            mp.copy_children()

            self.master_patient = mp
            empi = EMPI(None, controler=settings.EMPI_CONTROLER)
            empi.update_patient(empi.serialize(mp), mp.unique_id)

        return mp

    def copy_children(self):
        '''If Patient is a Master Patient, copy all objects that referenced its OPs to reference this MP.
           (Ex: Copy Addresses, Contacts, Documents, Parents and so on from its children.)

        Args:
            <none>

        Returns:
            <none>
        '''
        if self.is_master_patient:
            original_patients = Patient.objects.filter(unique_id=self.unique_id).exclude(id=self.id)
            for original_patient in original_patients:
                for related_object in [f for f in self._meta.related_objects]:
                    if hasattr(related_object.related_model, 'copy_to') and related_object.name not in ['inheriteds']:
                        for item in getattr(original_patient, related_object.name).all():
                            item.copy_to(self)

    def age(self, date=datetime.date.today()):
        '''Return the age of the patient in date informed. If date is not informed uses today.

        Args:
            date (date): (optional) The base date.

        Returns:
            The age of the patient on that date.
        '''

        age = relativedelta(date, self.date_birth).years if self.date_birth is not None else None
        return age

    def set_unique_id(self, token, unique_id, empi_type=AUTOMATIC):
        if self.unique_id == '':
            if token == (str(self.data_source) + '.' + self.original_id) and unique_id != '':
                logger.info(f'Set unique_id {unique_id} to patient {self.full_name}.')
                self.unique_id = unique_id
                self.empi_type = empi_type
                self.save()
                for exam in self.exams.all():
                    exam.save()
                    for f in exam.examfiles.all():
                        f.save()
                    if exam.examfiles.all().exists():
                        logger.info('Function "set_unique_id" is going to require severity.')
                        exam.require_severity()
                    for mr in exam.medical_reports.all():
                        if mr.physician.patient.master_patient is not None:
                            mr.save()
                ProfessionType = apps.get_model('professionals', 'ProfessionType')
                for prof in self.professions.filter(profession_type__special=ProfessionType.PHYSICIAN):
                    for mr in prof.medical_reports.all():
                        if mr.exam.patient.master_patient is not None:
                            mr.save()

    def run_empi(self, patient):
        if self.data_source.identifier not in ['AILA', 'CDP']:
            empi = EMPI(self.set_unique_id, controler=settings.EMPI_CONTROLER)
            empi.find_unique_id(empi.serialize(patient))


class Parent(ReplicableCDPModel, models.Model):
    '''
    Parents of a patient.
    '''
    FATHER = 'F'
    MOTHER = 'M'
    PARENT_TYPES = (
        (FATHER, 'Father'),
        (MOTHER, 'Mother')
    )
    patient = models.ForeignKey(Patient, related_name='parents', on_delete=models.CASCADE)
    parent_type = models.CharField(max_length=1, choices=PARENT_TYPES, help_text='M - Mother | F - Father')
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['patient__id', 'parent_type', 'name']
        indexes = [
            models.Index(fields=['patient', 'parent_type', 'name']),
            models.Index(fields=['parent_type', 'patient', 'name']),
        ]

    def __str__(self):
        return f'{self.name}, {self.get_parent_type_display().lower()} of {str(self.patient)}'

    def clean(self, *args, **kwargs):
        # Assert that the patient has only one mother and father.
        if not self.patient.is_master_patient:
            if self.parent_type == Parent.MOTHER and self.patient.get_mother().exclude(id=self.id).count() != 0:
                raise ValidationError('An original patient can only have one mother.')
            if self.parent_type == Parent.FATHER and self.patient.get_father().exclude(id=self.id).count() != 0:
                raise ValidationError('An original patient can only have one father.')
        super(Parent, self).clean(*args, **kwargs)

    def is_equal(self, obj):
        return self.name == obj.name and self.parent_type == obj.parent_type

    def save(self, *args, **kwargs):
        super(Parent, self).save(*args, **kwargs)
        if self.patient.is_master_patient:
            from .serializers import ParentSerializer
            self.upload_to_cdp(ParentSerializer)


class Address(ReplicableCDPModel, models.Model):
    '''
    A address of a patient or of a source.
    '''
    patient = models.ForeignKey(Patient, related_name='addresses', blank=True, null=True, on_delete=models.CASCADE)
    source = models.ForeignKey(
        'sources.Source', related_name='addresses', blank=True, null=True, on_delete=models.CASCADE
    )
    city = models.ForeignKey(City, related_name='addresses', on_delete=models.PROTECT, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, default='')
    district = models.CharField(max_length=100, blank=True, default='',
                                help_text='Name of the district or the neighborhood')
    street = models.CharField(max_length=200, blank=True, default='')
    number = models.CharField(blank=True, default='', max_length=10)
    complement = models.CharField(max_length=100, blank=True, default='')

    objects = AddressManager()

    class Meta:
        verbose_name_plural = 'addresses'
        ordering = ['patient__id', 'id']
        indexes = [
            models.Index(fields=['patient', 'zip_code', 'city', 'district']),
            models.Index(fields=['patient', 'city', 'district', 'zip_code']),
            models.Index(fields=['source', 'zip_code', 'city', 'district']),
            models.Index(fields=['source', 'city', 'district', 'zip_code']),
            models.Index(fields=['patient'])
        ]

    def __str__(self):
        return self.complete_address()

    def clean(self, *args, **kwargs):
        if self.patient is None and self.source is None:
            raise ValidationError('The address must have a patient or a source present.')
        if self.patient is not None and self.source is not None:
            raise ValidationError('Only one of the fields patient/source must be present.')
        super(Address, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        # If it is the address of a patient, follow the normal ReplicableCDPModel saving process
        # (save to master patient). If don't, just use the regular saving process.
        if self.patient is not None:
            super(Address, self).save(*args, **kwargs)
            if self.patient.is_master_patient:
                from .serializers import AddressSerializer
                self.upload_to_cdp(AddressSerializer)
        else:
            super(CDPModel, self).save(*args, **kwargs)

    def is_equal(self, obj):
        return str(self) in str(obj) or str(obj) in str(self)

    def copy_to(self, patient):
        '''Copy current Address to patient informed.

        Args:
            patient (patients.Patient): The patient to copy the Parent

        Returns:
            <none>
        '''
        add = True
        for address in patient.addresses.all():
            if str(self) in str(address):
                add = False
            else:
                if str(address) in str(self):
                    address.delete()
        if add:
            self._deep_copy(patient)

    def formatted_zipcode(self):
        '''Return formatted zip code.

        Args:
            <none>
        Returns:
            The zip code in Google Maps format.
        '''
        zipcode = re.sub(r'[^0-9]', '', self.zip_code).ljust(8, '0')
        return '{}-{}'.format(zipcode[:5], zipcode[5:])

    def complete_address(self):
        '''Return the complete address.

        Args:
            <none>
        Returns:
            The complete address (in Google Maps format).
        '''
        adr = ''
        if self.street is not None and self.street != '':
            adr = self.street
        if self.number != '':
            adr += (', ' if adr else '') + self.number
        if self.complement is not None and self.complement != '':
            adr += (' - ' if adr else '') + self.complement
        if self.district is not None and self.district != '':
            adr += (' - ' if adr else '') + self.district
        if self.city is not None:
            adr += (', ' if adr else '') + str(self.city)
        if self.zip_code is not None and self.zip_code != '':
            adr += (', ' if adr else '') + self.formatted_zipcode()
        return adr


class ContactType(CDPModel, models.Model):
    '''
    Type of the contact with patient. Ex: E-mail, Cellphone, etc.
    '''
    name = models.SlugField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True, default='')
    no_chr_in_disp = models.BooleanField(default=True, help_text='Show only numbers in display')

    class Meta:
        verbose_name_plural = 'contact types'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Contact(ReplicableCDPModel, models.Model):
    '''
    Contacts of the patient.
    '''
    contact_type = models.ForeignKey(ContactType, related_name='type_contacts', on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, related_name='contacts', blank=True, null=True, on_delete=models.CASCADE)
    source = models.ForeignKey(
        'sources.Source', related_name='contacts', blank=True, null=True, on_delete=models.CASCADE
    )
    value = models.CharField(max_length=100)
    comments = models.CharField(max_length=2000, blank=True, default='')

    objects = ContactManager()

    class Meta:
        ordering = ['contact_type__id', 'patient__id', 'value']
        indexes = [
            models.Index(fields=['patient', 'value']),
            models.Index(fields=['contact_type', 'patient', 'value']),
            models.Index(fields=['contact_type', 'value']),
        ]

    def __str__(self):
        val = re.sub(r'[^0-9+]', '', self.value) if self.contact_type.no_chr_in_disp else self.value
        return self.contact_type.name + ': ' + val

    def clean(self, *args, **kwargs):
        if self.patient is None and self.source is None:
            raise ValidationError('The contact must have a patient or a source present.')
        if self.patient is not None and self.source is not None:
            raise ValidationError('Only one of the fields patient/source must be present.')
        super(Contact, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        # If it is the contact of a patient, follow the normal ReplicableCDPModel saving process
        # (save to master patient). If don't, just use the regular saving process.
        if self.patient is not None:
            super(Contact, self).save(*args, **kwargs)
            if self.patient.is_master_patient:
                from .serializers import ContactSerializer
                self.upload_to_cdp(ContactSerializer)
        else:
            super(CDPModel, self).save(*args, **kwargs)


class DocumentType(CDPModel, models.Model):
    '''
    Type of the document of the patient. Ex: CPF, RG, etc.
    '''
    name = models.SlugField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        verbose_name_plural = 'document types'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Document(ReplicableCDPModel, models.Model):
    '''
    Documents of a patient or a source.
    '''
    document_type = models.ForeignKey(DocumentType, related_name='type_documents', on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, related_name='documents', blank=True, null=True, on_delete=models.CASCADE)
    source = models.ForeignKey(
        'sources.Source', related_name='documents', blank=True, null=True, on_delete=models.CASCADE
    )
    number = models.CharField(max_length=30)
    comments = models.CharField(max_length=2000, blank=True, default='')
    validity = models.DateField(null=True, blank=True)

    @property
    def clean_number(self):
        return re.sub(r'[^0-9]', '', self.number)

    objects = DocumentManager()

    class Meta:
        ordering = ['document_type__id', 'patient__id', 'number']
        indexes = [
            models.Index(fields=['patient', 'number']),
            models.Index(fields=['document_type', 'patient', 'number']),
            models.Index(fields=['document_type', 'number']),
            models.Index(fields=['patient', 'document_type', 'number'])
        ]

    def __str__(self):
        return self.document_type.name + ': ' + self.clean_number

    def clean(self, *args, **kwargs):
        if self.patient is None and self.source is None:
            raise ValidationError('The document must have a patient or a source present.')
        if self.patient is not None and self.source is not None:
            raise ValidationError('Only one of the fields patient/source must be present.')
        super(Document, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        # If it is the document of a patient, follow the normal ReplicableCDPModel saving process
        # (save to master patient). If don't, just use the regular saving process.
        if self.patient is not None:
            super(Document, self).save(*args, **kwargs)
            if self.patient.is_master_patient:
                from .serializers import DocumentSerializer
                self.upload_to_cdp(DocumentSerializer)
        else:
            super(CDPModel, self).save(*args, **kwargs)


@receiver(post_delete, sender=Parent)
def _parent_delete(sender, instance, **kwargs):
    try:
        if instance.patient.is_master_patient:
            instance.delete_on_cdp()
        else:
            # Check if MP's instance should be deleted
            mp = instance.patient.master_patient
            if mp is not None:
                keep_mp_parents = False
                op_parents = Parent.objects.filter(
                    patient__unique_id=mp.unique_id,
                    parent_type=instance.parent_type
                ).exclude(patient=mp)
                keep_mp_parents = True if any([op_parent.is_equal(instance) for op_parent in op_parents]) else False

                # Find MP's analogous instance and delete it
                if not keep_mp_parents:
                    for mp_parent in Parent.objects.filter(patient=mp):
                        if mp_parent.is_equal(instance):
                            mp_parent.delete()
    except Patient.DoesNotExist:
        pass


@receiver(post_delete, sender=Address)
def _address_delete(sender, instance, **kwargs):
    try:
        # If it is the address of a patient
        if instance.patient is not None:
            if instance.patient.is_master_patient:
                instance.delete_on_cdp()
            else:
                # Check if the address being deleted is present in the MP, therefore could be replaced
                # by one of its OPs less complete address.
                mp = instance.patient.master_patient
                if mp is not None:
                    replace = False
                    for mp_address in Address.objects.filter(patient=mp):
                        if str(mp_address) == str(instance):
                            mp_analogous_address = mp_address
                            replace = True

                    # Replace MP's address by the first less complete address from its OPs found
                    if replace:
                        mp_analogous_address.delete()
                        for op_address in Address.objects.filter(patient__unique_id=mp.unique_id).exclude(patient=mp):
                            if instance.is_more_complete(op_address):
                                op_address.copy_to(mp)
                                break
    except Patient.DoesNotExist:
        pass


@receiver(post_delete, sender=Contact)
def _contact_delete(sender, instance, **kwargs):
    try:
        if instance.patient is not None:
            if instance.patient.is_master_patient:
                instance.delete_on_cdp()
            else:
                mp = instance.patient.master_patient
                if mp is not None:
                    for cont in Contact.objects.filter(patient=mp, contact_type=instance.contact_type):
                        if str(instance) == str(cont):
                            mp_contact = cont
                    contacts = (
                        Contact.objects.filter(patient__unique_id=mp.unique_id, contact_type=instance.contact_type)
                        .exclude(patient=mp)
                    )
                    delete = True
                    for contact in contacts:
                        if str(contact) == str(instance):
                            delete = False
                    if delete:
                        mp_contact.delete()
    except Patient.DoesNotExist:
        pass


@receiver(post_delete, sender=Document)
def _document_delete(sender, instance, **kwargs):
    try:
        if instance.patient is not None:
            if instance.patient.is_master_patient:
                instance.delete_on_cdp()
            else:
                # Check if MP's instance should be deleted
                mp = instance.patient.master_patient
                keep_masters_instance = False
                if mp is not None:
                    op_documents = Document.objects.filter(
                        patient__unique_id=mp.unique_id,
                        document_type=instance.document_type
                    ).exclude(patient=mp)
                    keep_masters_instance = (
                        True if any([op_doc.is_equal(instance) for op_doc in op_documents]) else False
                    )

                # Find MP's analogous instance and delete it
                if not keep_masters_instance:
                    for mp_document in Document.objects.filter(patient=mp):
                        if mp_document.is_equal(instance):
                            mp_document.delete()
    except Patient.DoesNotExist:
        pass


@receiver(post_delete, sender=Patient)
def _patient_delete(sender, instance, **kwargs):
    if instance.data_source is not None:
        mp = instance.master_patient
        if mp is not None and mp.original_patients.all().count() == 0:
            empi = EMPI(None, controler=settings.EMPI_CONTROLER)
            empi.delete_patient(mp.unique_id)
            mp.delete_on_cdp(model_name='Master Patient')
            mp.delete()
