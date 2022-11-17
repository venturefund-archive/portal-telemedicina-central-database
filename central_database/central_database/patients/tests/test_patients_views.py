from unittest import mock

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from central_database.patients.tests.mocked_fhir_responses import (
    all_patients,
    patient_detail,
)
from central_database.users.tests.factories import UserFactory


class TestPatientViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    @mock.patch(
        "central_database.patients.api.views.patient_resource.service.PatientService.get_all"
    )
    def test_it_requires_authentication(self, mock_get):
        mock_get.return_value = all_patients
        response = self.client.get(reverse("api:patients-list"))

        self.assertEqual(response.status_code, 403)

    @mock.patch(
        "central_database.patients.api.views.patient_resource.service.PatientService.get_all"
    )
    def test_it_lists_patients(self, mock_get):
        mock_get.return_value = all_patients

        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("api:patients-list"))

        self.assertEqual(response.status_code, 200)

    @mock.patch(
        "central_database.patients.api.views.patient_resource.service.PatientService.get_detail"
    )
    def test_it_retrieves_patient_detail(self, mock_get):
        mock_get.return_value = patient_detail

        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("api:patients-detail", kwargs={"pk": 4172}))

        self.assertEqual(response.status_code, 200)
