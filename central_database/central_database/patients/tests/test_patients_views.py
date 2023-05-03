from unittest import mock

from fhirclient.models.patient import Patient
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from central_database.customers.factories import ClientFactory
from central_database.patients.tests.factories import PatientFactory
from central_database.permissions_manager.models import Role
from central_database.users.tests.factories import UserFactory
from central_database.vaccines.tests.factories import (
    VaccineAlertFactory,
    VaccineAlertTypeFactory,
    VaccineDoseFactory,
    VaccineProtocolFactory,
)


class TestPatientViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        base_role = Role.objects.get(slug="healthcare-manager")
        self.role = base_role.create_role_from_base_role(
            client=ClientFactory()
        )  # noqa: E501
        self.role.assign_to_user(self.user)

    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet.get_queryset"  # noqa: E501
    )
    def test_it_requires_authentication(self, mock_get):
        response = self.client.get(reverse("api:patients-list"))

        self.assertEqual(response.status_code, 401)

    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet._get_fhir_client"  # noqa: E501
    )
    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet.get_queryset"  # noqa: E501
    )
    def test_it_requires_patient_view_permission(
        self, mock_get, mock_get_fhir_client
    ):  # noqa: E501
        user_without_permission = UserFactory()

        mock_fhir_client = mock.MagicMock()
        mock_get_fhir_client.return_value = mock_fhir_client

        self.client.force_authenticate(user_without_permission)
        response = self.client.get(reverse("api:patients-list"))

        self.assertEqual(response.status_code, 403)

    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet._get_fhir_client"  # noqa: E501
    )
    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet.get_queryset"  # noqa: E501
    )
    def test_it_lists_patients(self, mock_get, mock_get_fhir_client):

        queryset = [PatientFactory() for _ in range(2)]
        self.vaccine_dose_1 = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        self.vaccine_dose_2 = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )

        self.vaccine_alert_type = VaccineAlertTypeFactory()
        self.vaccine_alert_1 = VaccineAlertFactory(
            patient_id=queryset[0].id,
            vaccine_dose=self.vaccine_dose_1,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )
        self.vaccine_alert_2 = VaccineAlertFactory(
            patient_id=queryset[1].id,
            vaccine_dose=self.vaccine_dose_2,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )

        self.protocol = VaccineProtocolFactory(
            vaccine_doses=[self.vaccine_dose_1, self.vaccine_dose_2]
        )
        mock_get.return_value = queryset

        mock_fhir_client = mock.MagicMock()
        mock_get_fhir_client.return_value = mock_fhir_client

        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("api:patients-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        for data in response.data:
            self.assertTrue("id" in data)
            self.assertTrue("birth_date" in data)
            self.assertTrue("name" in data)
            self.assertTrue("number_of_alerts_by_protocol" in data)
            self.assertTrue("age_in_days" in data)

    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet._get_fhir_client"  # noqa: E501
    )
    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet.get_object"  # noqa: E501
    )
    def test_it_retrieves_a_patient_detail(
        self, mock_get, mock_get_fhir_client
    ):  # noqa: E501
        patient = PatientFactory()
        mock_get.return_value = patient

        mock_fhir_client = mock.MagicMock()
        mock_get_fhir_client.return_value = mock_fhir_client

        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse("api:patients-detail", kwargs={"pk": patient.id})
        )  # noqa: E501

        self.assertEqual(response.status_code, 200)
        keys = [
            "id",
            "name",
            "telecom",
            "gender",
            "birth_date",
            "address",
            "marital_status",
        ]
        for key in keys:
            self.assertTrue(key in response.data)


class TestPatientUpdateViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        base_role = Role.objects.get(slug="healthcare-manager")
        self.role = base_role.create_role_from_base_role(
            client=ClientFactory()
        )  # noqa: E501
        self.role.assign_to_user(self.user)

    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet._get_fhir_client"  # noqa: E501
    )
    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet.get_object"  # noqa: E501
    )
    def test_it_requires_patient_change_permission(
        self, mock_get, mock_get_fhir_client
    ):
        user_without_permission = UserFactory()

        patient = PatientFactory()
        mock_get.return_value = patient

        mock_fhir_client = mock.MagicMock()
        mock_get_fhir_client.return_value = mock_fhir_client

        payload = {"gender": "male"}
        self.client.force_authenticate(user_without_permission)
        response = self.client.patch(
            reverse("api:patients-detail", kwargs={"pk": patient.id}),
            data=payload,
            format="json",
        )  # noqa: E501

        self.assertEqual(response.status_code, 403)

    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet._get_fhir_client"  # noqa: E501
    )
    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet.get_object"
    )  # noqa: E501
    @mock.patch.object(Patient, "update")
    def test_it_updates_patient(
        self, mock_update, mock_get_object, mock_get_fhir_client
    ):
        test_patient = PatientFactory()

        mock_get_object.return_value = test_patient
        mock_fhir_client = mock.MagicMock()
        mock_get_fhir_client.return_value = mock_fhir_client

        payload = {
            "resource_type": "Patient",
            "id": test_patient.id,
            "birth_date": "2023-01-06",
            "name": "TEST PATIENT NAME",
            "gender": "female",
            "telecom": None,
            "marital_status": None,
            "address": [
                {
                    "id": 1,
                    "line": ["123 Main St"],
                    "city": "Anytownaa",
                    "state": "CA",
                    "postal_code": "68232422",
                    "country": "BRAZIL",
                    "latitude": 100,
                    "longitude": 100,
                }
            ],
        }

        self.client.force_authenticate(self.user)
        response = self.client.patch(
            reverse("api:patients-detail", kwargs={"pk": test_patient.id}),
            data=payload,
            format="json",
        )

        mock_update.update.assert_not_called()

        self.assertEqual(response.status_code, 200)

    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet._get_fhir_client"  # noqa: E501
    )
    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet.get_object"
    )  # noqa: E501
    @mock.patch.object(Patient, "update")
    def test_it_updates_patient_partially(
        self, mock_update, mock_get_object, mock_get_fhir_client
    ):
        test_patient = PatientFactory()

        mock_get_object.return_value = test_patient

        mock_fhir_client = mock.MagicMock()
        mock_get_fhir_client.return_value = mock_fhir_client

        payload = {"gender": "male"}

        self.client.force_authenticate(self.user)
        response = self.client.patch(
            reverse("api:patients-detail", kwargs={"pk": test_patient.id}),
            data=payload,
            format="json",
        )

        mock_update.update.assert_not_called()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["gender"], "male")

    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet._get_fhir_client"  # noqa: E501
    )
    @mock.patch(
        "central_database.patients.api.views.PatientsViewSet.get_object"
    )  # noqa: E501
    @mock.patch.object(Patient, "update")
    def test_update_coordinates(
        self, mock_update, mock_get_object, mock_get_fhir_client
    ):
        test_patient = PatientFactory()

        mock_get_object.return_value = test_patient

        mock_fhir_client = mock.MagicMock()
        mock_get_fhir_client.return_value = mock_fhir_client

        payload = {"address": [{"id": 1, "latitude": 100, "longitude": 101}]}

        self.client.force_authenticate(self.user)
        response = self.client.patch(
            reverse("api:patients-detail", kwargs={"pk": test_patient.id}),
            data=payload,
            format="json",
        )

        mock_update.update.assert_not_called()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["address"][0].get("latitude"), 100)
        self.assertEqual(response.data["address"][0].get("longitude"), 101)
