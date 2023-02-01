import factory

from central_database.customers.factories import ClientFactory
from central_database.permissions_manager.models import Role


class RoleFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("pystr")
    slug = factory.Faker("pystr")

    client = factory.SubFactory(ClientFactory)

    class Meta:
        model = Role
