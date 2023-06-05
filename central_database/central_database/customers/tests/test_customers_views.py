import json

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from central_database.customers.factories import (  # noqa: E501
    ClientFactory,
    MicroRegionFactory,
)
from central_database.users.tests.factories import UserFactory


class TestMicroRegionViewSet(APITestCase):
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

    def test_it_create_microregions(self):
        payload = {
            "name": "test1",
            "polygon": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [100.0, 0.0],
                        [101.0, 0.0],
                        [101.0, 1.0],
                        [110.0, 1.0],
                        [100.0, 0.0],
                    ]
                ],
            },
            "client": self.client_customer.id,
        }
        url = reverse("api:microregion-list")

        self.client.force_authenticate(self.user)
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.content)
        self.assertEqual(data["type"], "Feature")

    def test_it_updates_microregions(self):
        micro_region = MicroRegionFactory(client=self.client_customer)
        payload = {
            "name": micro_region.name,
            "polygon": {
                "type": "Polygon",
                "coordinates": [
                    [[0.0, 0.0], [0.0, 1.1], [1.0, 1.0], [0.0, 0.0]]
                ],  # noqa: E501
            },
            "client": micro_region.client.id,
        }
        url = reverse("api:microregion-detail", kwargs={"pk": micro_region.id})

        self.client.force_authenticate(self.user)
        response = self.client.put(url, data=payload, format="json")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data["type"], "Feature")
        self.assertEqual(data["geometry"]["coordinates"][0][1][1], 1.1)

    def test_it_partial_updates_microregions(self):
        micro_region = MicroRegionFactory(client=self.client_customer)
        payload = {
            "polygon": {
                "type": "Polygon",
                "coordinates": [
                    [[0.0, 0.0], [0.0, 1.1], [1.0, 1.0], [0.0, 0.0]]
                ],  # noqa: E501
            },
        }
        url = reverse("api:microregion-detail", kwargs={"pk": micro_region.id})

        self.client.force_authenticate(self.user)
        response = self.client.patch(url, data=payload, format="json")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data["type"], "Feature")
        self.assertEqual(data["geometry"]["coordinates"][0][1][1], 1.1)

    def test_it_deletes_microregion(self):
        micro_region = MicroRegionFactory(client=self.client_customer)
        url = reverse("api:microregion-detail", kwargs={"pk": micro_region.id})

        self.client.force_authenticate(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
