import factory

from customers.factories import ClientFactory
from permissions_manager.models import Role


class RoleFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("pystr")
    slug = factory.Faker("pystr")

    client = factory.SubFactory(ClientFactory)

    class Meta:
        model = Role
