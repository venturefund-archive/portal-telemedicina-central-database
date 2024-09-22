import factory.fuzzy
from django.contrib.gis.geos import Polygon

from customers.models import (  # noqa: E501
    Client,
    HealthProfessional,
    Dataset,
    FhirStore,
    MicroRegion,
)


class DatasetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dataset


class FhirStoreFactory(factory.django.DjangoModelFactory):
    dataset = factory.SubFactory(DatasetFactory)

    class Meta:
        model = FhirStore


class ClientFactory(factory.django.DjangoModelFactory):
    fhir_store = factory.SubFactory(FhirStoreFactory)
    client_name = factory.Faker("pystr")
    city = factory.Faker("pystr")

    class Meta:
        model = Client


class MicroRegionFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("pystr")
    polygon = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
    client = factory.SubFactory(ClientFactory)

    class Meta:
        model = MicroRegion


class HealthProfessionalFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("pystr")
    cns_number = factory.Faker("pystr", max_chars=16)
    cnes_number = factory.Faker("pystr", max_chars=16)
    client = factory.SubFactory(ClientFactory)

    class Meta:
        model = HealthProfessional
