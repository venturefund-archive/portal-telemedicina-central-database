import datetime

import factory.fuzzy
from patients.models import Patient, Vaccine, VaccineStatus


class PatientFactory(factory.django.DjangoModelFactory):
    full_name = factory.Faker("pystr")
    social_name = factory.Faker("pystr")
    date_birth = factory.fuzzy.FuzzyDate(start_date=datetime.date(1, 1, 1))
    sex = factory.fuzzy.FuzzyChoice(Patient.SEX, getter=lambda c: c[0])

    class Meta:
        model = Patient


class VaccineFactory(factory.django.DjangoModelFactory):
    limit_date = factory.fuzzy.FuzzyDate(start_date=datetime.date(1, 1, 1))
    name_of_vaccine = factory.Faker("pystr")

    class Meta:
        model = Vaccine


class VaccineStatusFactory(factory.django.DjangoModelFactory):
    patient = factory.SubFactory(PatientFactory)
    vaccine = factory.SubFactory(VaccineFactory)

    class Meta:
        model = VaccineStatus
