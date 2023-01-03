from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class HealthCheckTestCase(APITestCase):
    def test_it_succeeds(self):
        response = self.client.get(reverse("health:health-check"))
        self.assertEqual(response.status_code, 200)
