import factory.fuzzy

from central_database.vaccines.models import (
    Vaccine,
    VaccineAlert,
    VaccineAlertType,
    VaccineDose,
)


class VaccineFactory(factory.django.DjangoModelFactory):
    system = factory.fuzzy.FuzzyChoice(
        Vaccine.SYSTEM_VALUE_SETS, getter=lambda c: c[0]
    )  # noqa: E501
    code = factory.Faker("pyint")
    display = factory.Faker("pystr")
    description = factory.Faker("pystr")

    class Meta:
        model = Vaccine


class VaccineDoseFactory(factory.django.DjangoModelFactory):
    vaccine = factory.SubFactory(VaccineFactory)
    minimum_recommended_age = factory.Faker("pyint")
    maximum_recommended_age = factory.Faker("pyint")
    dose_order = factory.Faker("pyint")
    booster = factory.Faker("boolean")
    gender_recommendation = factory.fuzzy.FuzzyChoice(
        VaccineDose.GENDER_RECOMMENDATION, getter=lambda c: c[0]
    )

    class Meta:
        model = VaccineDose


class VaccineAlertTypeFactory(factory.django.DjangoModelFactory):
    description = factory.Faker("pystr")
    description_pt_br = factory.Faker("pystr")

    class Meta:
        model = VaccineAlertType


class VaccineAlertFactory(factory.django.DjangoModelFactory):
    vaccine_dose = factory.SubFactory(VaccineDoseFactory)
    patient_id = factory.Faker("pyint")
    alert_type = factory.SubFactory(VaccineAlertTypeFactory)

    class Meta:
        model = VaccineAlert
