import json
import urllib

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from central_database.customers.factories import ClientFactory
from central_database.permissions_manager.models import Role
from central_database.users.tests.factories import UserFactory
from central_database.vaccines.tests.factories import (
    VaccineAlertFactory,
    VaccineAlertTypeFactory,
    VaccineDoseFactory,
    VaccineFactory,
    VaccineProtocolFactory,
)


def build_url_with_query_params(reverse_string, query_params):
    query = urllib.parse.urlencode(query_params)
    url = f"{reverse(reverse_string)}?{query}"
    return url


class TestVaccineDoseViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        base_role = Role.objects.get(slug="healthcare-manager")
        role = base_role.create_role_from_base_role(client=ClientFactory())
        role.assign_to_user(self.user)

    def test_it_requires_authentication(self):
        response = self.client.get(reverse("api:vaccine-doses-list"))

        self.assertEqual(response.status_code, 401)

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


class VaccineAlertsCountTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.vaccine_dose_1 = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        self.vaccine_dose_2 = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        self.vaccine_dose_3 = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        self.vaccine_dose_4 = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )

        self.vaccine_alert_type = VaccineAlertTypeFactory()
        self.vaccine_alert_1 = VaccineAlertFactory(
            vaccine_dose=self.vaccine_dose_1,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )
        self.vaccine_alert_2 = VaccineAlertFactory(
            vaccine_dose=self.vaccine_dose_2,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )
        self.vaccine_alert_3 = VaccineAlertFactory(
            vaccine_dose=self.vaccine_dose_2,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )
        self.vaccine_alert_4 = VaccineAlertFactory(
            vaccine_dose=self.vaccine_dose_3,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )

        self.protocol = VaccineProtocolFactory(
            vaccine_doses=[self.vaccine_dose_1, self.vaccine_dose_2]
        )

    def test_retrieve_alerts_count(self):
        url = reverse(
            "api:vaccine-alerts-count-detail", kwargs={"pk": self.protocol.id}
        )
        self.client.force_authenticate(self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(
            response.data,
            {
                "id": self.protocol.id,
                "vaccine_doses": [
                    {
                        "id": self.vaccine_dose_1.id,
                        "vaccine": self.vaccine_dose_1.vaccine.id,
                        "dose_order": self.vaccine_dose_1.dose_order,
                        "gender_recommendation": self.vaccine_dose_1.gender_recommendation,  # noqa: E501
                        "alerts_count": 1,
                        "completed_amount": 0,
                        "completed_percentage": 0,
                    },
                    {
                        "id": self.vaccine_dose_2.id,
                        "vaccine": self.vaccine_dose_2.vaccine.id,
                        "dose_order": self.vaccine_dose_2.dose_order,
                        "gender_recommendation": self.vaccine_dose_2.gender_recommendation,  # noqa: E501
                        "alerts_count": 2,
                        "completed_amount": 0,
                        "completed_percentage": 0,
                    },
                ],
                "completed_doses_count": 0,
                "completed_doses_percentage": 0,
                "alert_doses_count": 3,
                "expected_doses_count": 3,
                "permissions": {},
            },
        )
