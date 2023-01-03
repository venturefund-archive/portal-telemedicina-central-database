import json
from unittest import mock

from django.conf import settings
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from central_database.users.tests.factories import UserFactory


class TestPatientViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    @mock.patch(
        "central_database.patients.api.views.patient_resource.service.PatientService.get_all"  # noqa: E501
    )
    def test_it_requires_authentication(self, mock_get):
        mock_get.return_value = json.load(
            open(
                f"{settings.CENTRAL_DATABASE_PATH}/patients/tests/fixtures/all_patients_fhir_responses.json"  # noqa: E501
            )
        )
        response = self.client.get(reverse("api:patients-list"))

        self.assertEqual(response.status_code, 401)

    @mock.patch(
        "central_database.patients.api.views.patient_resource.service.PatientService.get_all"  # noqa: E501
    )
    def test_it_lists_patients(self, mock_get):
        mock_get.return_value = json.load(
            open(
                f"{settings.CENTRAL_DATABASE_PATH}/patients/tests/fixtures/all_patients_fhir_responses.json"  # noqa: E501
            )
        )

        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("api:patients-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 20)
        for data in response.data:
            self.assertTrue("id" in data)
            self.assertTrue("name" in data)

    @mock.patch(
        "central_database.patients.api.views.patient_resource.service.PatientService.get_detail"  # noqa: E501
    )
    def test_it_retrieves_patient_detail(self, mock_get):
        mock_get.return_value = json.load(
            open(
                f"{settings.CENTRAL_DATABASE_PATH}/patients/tests/fixtures/patient_detail_fhir_response.json"  # noqa: E501
            )
        )

        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse("api:patients-detail", kwargs={"pk": 4172})
        )  # noqa: E501

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
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
