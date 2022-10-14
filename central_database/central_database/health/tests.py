from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from central_database.vaccines.factories import UserFactory


class HealthCheckTestCase(APITestCase):
    def test_it_succeeds(self):
        UserFactory()
        response = self.client.get(reverse('health-check'))
        self.assertEqual(response.status_code, 200)

    def test_it_fails(self):
        response = self.client.get(reverse('health-check'))
        self.assertEqual(response.status_code, 503)
