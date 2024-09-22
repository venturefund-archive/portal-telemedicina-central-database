import json
import urllib
from datetime import datetime

from dateutil.relativedelta import relativedelta
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from customers.factories import (
    ClientFactory,
    HealthProfessionalFactory,
)
from customers.models import HealthProfessional
from patients.tests.factories import PatientFactory
from permissions_manager.models import Role
from users.tests.factories import UserFactory
from vaccines.tests.factories import (
    VaccineAlertFactory,
    VaccineAlertTypeFactory,
    VaccineDoseFactory,
    VaccineFactory,
    VaccineProtocolFactory,
    VaccineStatusFactory,
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
            fhir_store=self.user.client.fhir_store,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )
        self.vaccine_alert_2 = VaccineAlertFactory(
            vaccine_dose=self.vaccine_dose_2,
            fhir_store=self.user.client.fhir_store,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )
        self.vaccine_alert_3 = VaccineAlertFactory(
            vaccine_dose=self.vaccine_dose_2,
            fhir_store=self.user.client.fhir_store,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )
        self.vaccine_alert_4 = VaccineAlertFactory(
            vaccine_dose=self.vaccine_dose_3,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )

        self.protocol = VaccineProtocolFactory(
            vaccine_doses=[self.vaccine_dose_1, self.vaccine_dose_2],
            client=self.user.client,
        )

    def test_retrieve_alerts_count(self):
        url = reverse(
            "api:vaccine-alerts-count-detail", kwargs={"pk": self.protocol.id}
        )
        self.client.force_authenticate(self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data,
            {
                "id": self.protocol.id,
                "vaccine_doses": [
                    {
                        "id": self.vaccine_dose_1.id,
                        "vaccine": {
                            "id": self.vaccine_dose_1.vaccine.id,
                            "name": self.vaccine_dose_1.vaccine.display,
                        },
                        "dose_order": self.vaccine_dose_1.dose_order,
                        "gender_recommendation": self.vaccine_dose_1.gender_recommendation,  # noqa: E501
                        "alerts_count": 1,
                        "completed_amount": 0,
                        "completed_percentage": 0,
                    },
                    {
                        "id": self.vaccine_dose_2.id,
                        "vaccine": {
                            "id": self.vaccine_dose_2.vaccine.id,
                            "name": self.vaccine_dose_2.vaccine.display,
                        },
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


class TestVaccineAlertViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_deactivate_alert(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )

        vaccine_alert_type = VaccineAlertTypeFactory()
        vaccine_alert = VaccineAlertFactory(
            vaccine_dose=vaccine_dose,
            alert_type=vaccine_alert_type,
            active=True,  # noqa: E501
        )

        url = reverse(
            "api:vaccine-alerts-deactivate-alert",
            kwargs={"pk": vaccine_alert.id},  # noqa: E501
        )

        self.client.force_authenticate(self.user)
        response = self.client.patch(url)
        vaccine_alert.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(vaccine_alert.active, False)
        self.assertEqual(response.data["active"], False)

    def test_activate_alert(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )

        vaccine_alert_type = VaccineAlertTypeFactory()
        vaccine_alert = VaccineAlertFactory(
            vaccine_dose=vaccine_dose,
            alert_type=vaccine_alert_type,
            active=False,  # noqa: E501
        )

        url = reverse(
            "api:vaccine-alerts-activate-alert",
            kwargs={"pk": vaccine_alert.id},  # noqa: E501
        )

        self.client.force_authenticate(self.user)
        response = self.client.patch(url)
        vaccine_alert.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(vaccine_alert.active, True)
        self.assertEqual(response.data["active"], True)

    def test_deactivate_non_existent_alert(self):
        url = reverse(
            "api:vaccine-alerts-deactivate-alert", kwargs={"pk": 99999}
        )  # noqa: E501

        self.client.force_authenticate(self.user)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 404)

    def test_activate_non_existent_alert(self):
        url = reverse(
            "api:vaccine-alerts-activate-alert", kwargs={"pk": 99999}
        )  # noqa: E501

        self.client.force_authenticate(self.user)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 404)


class TestVaccineStatusViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        base_role = Role.objects.get(slug="healthcare-manager")
        role = base_role.create_role_from_base_role(client=ClientFactory())
        role.assign_to_user(self.user)

    def test_it_creates_vaccine_status(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        patient = PatientFactory()

        date_now = datetime.now()

        payload = {
            "batch": "test",
            "patient_id": patient.id,
            "completed": True,
            "application_date": date_now.strftime("%Y-%m-%d"),
            "next_dose_application_date": (
                date_now + relativedelta(months=+1)
            ).strftime("%Y-%m-%d"),
            "vaccine_dose": vaccine_dose.id,
        }
        url = reverse("api:vaccine-status-list")
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_it_creates_vaccine_status_with_health_professional_info(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        patient = PatientFactory()

        date_now = datetime.now()

        payload = {
            "batch": "test",
            "patient_id": patient.id,
            "completed": True,
            "application_date": date_now.strftime("%Y-%m-%d"),
            "next_dose_application_date": (
                date_now + relativedelta(months=+1)
            ).strftime("%Y-%m-%d"),
            "vaccine_dose": vaccine_dose.id,
            "health_professional": {
                "name": "Professional Name",
                "cns_number": "1234567890",
            },
        }
        url = reverse("api:vaccine-status-list")
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_it_prevents_create_existing_health_professional_when_create_vaccine_status(  # noqa: E501
        self,
    ):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        patient = PatientFactory()

        date_now = datetime.now()

        health_professional = HealthProfessionalFactory()
        payload = {
            "batch": "test",
            "patient_id": patient.id,
            "completed": True,
            "application_date": date_now.strftime("%Y-%m-%d"),
            "next_dose_application_date": (
                date_now + relativedelta(months=+1)
            ).strftime("%Y-%m-%d"),
            "vaccine_dose": vaccine_dose.id,
            "health_professional": {
                "name": health_professional.name,
                "cns_number": health_professional.cns_number,
            },
        }
        url = reverse("api:vaccine-status-list")
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HealthProfessional.objects.all().count(), 1)

    def test_it_updates_vaccine_status(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        vaccine_status = VaccineStatusFactory(vaccine_dose=vaccine_dose)

        date_now = datetime.now()

        url = reverse(
            "api:vaccine-status-detail", kwargs={"pk": vaccine_status.id}
        )  # noqa: E501
        self.client.force_authenticate(self.user)
        payload = {
            "batch": "new_batch",
            "patient_id": vaccine_status.patient_id,
            "completed": True,
            "application_date": date_now.strftime("%Y-%m-%d"),
            "next_dose_application_date": (
                date_now + relativedelta(months=+1)
            ).strftime("%Y-%m-%d"),
            "vaccine_dose": vaccine_dose.id,
            "health_professional": {
                "name": "New Name",
                "cns_number": "New CNS Number",
            },  # noqa: E501
        }
        response = self.client.put(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["batch"], "new_batch")

    def test_it_partially_update_vaccine_status(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        vaccine_status = VaccineStatusFactory(
            vaccine_dose=vaccine_dose, completed=False
        )
        url = reverse(
            "api:vaccine-status-detail", kwargs={"pk": vaccine_status.id}
        )  # noqa: E501
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            url, data={"completed": True}, format="json"
        )  # noqa: E501
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["completed"])

    def test_it_deletes_vaccine_status(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        vaccine_status = VaccineStatusFactory(vaccine_dose=vaccine_dose)
        url = reverse(
            "api:vaccine-status-detail", kwargs={"pk": vaccine_status.id}
        )  # noqa: E501
        self.client.force_authenticate(self.user)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
