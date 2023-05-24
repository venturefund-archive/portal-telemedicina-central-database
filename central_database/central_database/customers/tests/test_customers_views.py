import json

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from central_database.customers.factories import (  # noqa: E501
    ClientFactory,
    MicroRegionFactory,
)
from central_database.users.tests.factories import UserFactory


class TestVaccineDoseViewSet(APITestCase):
    def setUp(self):
        self.client_customer = ClientFactory()
        self.user = UserFactory(client=self.client_customer)

    def test_it_requires_authentication(self):
        response = self.client.get(reverse("api:microregion-list"))

        self.assertEqual(response.status_code, 401)

    def test_it_list_microregions(self):
        MicroRegionFactory(client=self.client_customer)

        url = reverse("api:microregion-list")

        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        print(data)
        self.assertEqual(len(data["features"]), 1)

    def test_it_does_not_list_microregion_from_another_client(self):
        MicroRegionFactory(client=self.client_customer)
        client_with_no_microregions = ClientFactory()
        user_from_another_client = UserFactory(
            client=client_with_no_microregions
        )  # noqa: E501
        url = reverse("api:microregion-list")

        self.client.force_authenticate(user_from_another_client)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data["features"]), 0)
