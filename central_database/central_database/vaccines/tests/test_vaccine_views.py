import json
import urllib

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from central_database.users.tests.factories import UserFactory
from central_database.vaccines.tests.factories import (
    VaccineAlertFactory,
    VaccineDoseFactory,
    VaccineFactory,
)


def build_url_with_query_params(reverse_string, query_params):
    query = urllib.parse.urlencode(query_params)
    url = f"{reverse(reverse_string)}?{query}"
    return url


class TestVaccineDoseViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_it_requires_authentication(self):
        response = self.client.get(reverse("api:vaccine-doses-list"))

        self.assertEqual(response.status_code, 403)

    def test_it_list_vaccine_doses(self):
        vaccine = VaccineFactory()
        VaccineDoseFactory(
            vaccine=vaccine,
            booster=True,
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        VaccineDoseFactory(
            vaccine=vaccine,
            booster=True,
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )

        url = reverse("api:vaccine-doses-list")

        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_it_list_vaccine_doses_with_alerts(self):
        vaccine = VaccineFactory()
        vaccine_dose_1 = VaccineDoseFactory(
            vaccine=vaccine,
            booster=True,
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        VaccineDoseFactory(
            vaccine=vaccine,
            booster=True,
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )

        vaccine_alert_1 = VaccineAlertFactory(
            vaccine_dose=vaccine_dose_1, patient_id=11
        )
        vaccine_alert_1.save()
        query_params = {"patient_id": 11}
        url = build_url_with_query_params(
            "api:vaccine-doses-list", query_params
        )  # noqa: E501

        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        alerts = data[0].get("alerts")
        self.assertEqual(len(alerts), 1)
