import factory.fuzzy

from central_database.customers.models import Client


class ClientFactory(factory.django.DjangoModelFactory):
    dataset_id = factory.Faker("pystr")
    fhir_store_id = factory.Faker("pystr")
    client_name = factory.Faker("pystr")

    ibge_population = factory.Faker("pyint")
    children_born_alive = factory.Faker("pyint")
    children_registered_in_APS = factory.Faker("pyint")
    sisab_municipal_registration = factory.Faker("pyint")

    class Meta:
        model = Client
