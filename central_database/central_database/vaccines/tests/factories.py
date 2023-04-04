import factory.fuzzy

from central_database.customers.factories import ClientFactory
from central_database.vaccines.models import (
    Vaccine,
    VaccineAlert,
    VaccineAlertType,
    VaccineDose,
    VaccineProtocol,
    VaccineProtocolClient,
    VaccineStatus,
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


class VaccineStatusFactory(factory.django.DjangoModelFactory):
    vaccine_dose = factory.SubFactory(VaccineDoseFactory)
    patient_id = factory.Faker("pyint")
    completed = factory.Faker("boolean")

    class Meta:
        model = VaccineStatus


class VaccineProtocolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VaccineProtocol

    @factory.post_generation
    def vaccine_doses(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for vaccine_dose in extracted:
                self.vaccine_doses.add(vaccine_dose)


class VaccineProtocolClientFactory(factory.django.DjangoModelFactory):
    client = factory.SubFactory(ClientFactory)
    protocol = factory.SubFactory(VaccineProtocolFactory)

    class Meta:
        model = VaccineProtocolClient
