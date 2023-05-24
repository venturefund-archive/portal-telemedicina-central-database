import factory.fuzzy

from central_database.customers.models import Client


class ClientFactory(factory.django.DjangoModelFactory):
    dataset_id = factory.Faker("pystr")
    fhir_store_id = factory.Faker("pystr")
    client_name = factory.Faker("pystr")
    city = factory.Faker("pystr")

    class Meta:
        model = Client
