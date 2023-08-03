from unittest.mock import MagicMock

from rest_framework.test import APITestCase

from central_database.patients.api.serializers import PatientSerializer
from central_database.patients.helpers import calculate_age_in_days
from central_database.patients.tests.factories import PatientFactory
from central_database.users.tests.factories import UserFactory
from central_database.vaccines.models import VaccineAlert
from central_database.vaccines.tests.factories import (
    VaccineAlertFactory,
    VaccineAlertTypeFactory,
    VaccineDoseFactory,
    VaccineProtocolFactory,
)


class TestPatientSerializer(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_it_serializes_all_fields_for_patient(self):
        patient = PatientFactory()

        serialized_patient = PatientSerializer(patient).data
        parts = []
        patient_name = patient.name[0]
        if patient_name.given:
            parts.extend(patient_name.given)
        if patient_name.family:
            parts.append(patient_name.family)
        name = " ".join(parts)

        self.assertEqual(serialized_patient["id"], patient.id)
        self.assertEqual(
            serialized_patient["birth_date"],
            patient.birthDate.date.strftime("%Y-%m-%d"),
        )
        self.assertEqual(serialized_patient["name"], name)
        self.assertEqual(serialized_patient["gender"], patient.gender)
        self.assertIn("address", serialized_patient.keys())

        self.assertEqual(
            serialized_patient["address"]["line"], patient.address[0].line
        )  # noqa: E501
        self.assertEqual(
            serialized_patient["address"]["city"], patient.address[0].city
        )  # noqa: E501
        self.assertEqual(
            serialized_patient["address"]["state"], patient.address[0].state
        )
        self.assertEqual(
            serialized_patient["address"]["postal_code"],
            patient.address[0].postalCode,  # noqa: E501
        )
        self.assertEqual(
            serialized_patient["address"]["country"],
            patient.address[0].country,  # noqa: E501
        )
        for extension in patient.address[0].extension[0].extension:
            self.assertEqual(
                serialized_patient["address"][extension.url],
                extension.valueDecimal,  # noqa: E501
            )

        return serialized_patient

    def test_it_serializes_only_some_fields_for_patient_list(self):

        patient_1 = PatientFactory()
        patient_2 = PatientFactory()
        resources = [patient_1, patient_2]
        vaccine_doses = [
            VaccineDoseFactory(
                minimum_recommended_age=1,
                maximum_recommended_age=2,
            )
            for _ in range(2)
        ]

        self.vaccine_alert_type = VaccineAlertTypeFactory()
        self.vaccine_alert_1 = VaccineAlertFactory(
            patient_id=patient_1.id,
            vaccine_dose=vaccine_doses[0],
            fhir_store=self.user.client.fhir_store,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )
        self.vaccine_alert_2 = VaccineAlertFactory(
            patient_id=patient_2.id,
            vaccine_dose=vaccine_doses[1],
            fhir_store=self.user.client.fhir_store,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )

        self.protocol = VaccineProtocolFactory(
            vaccine_doses=vaccine_doses, client=self.user.client
        )

        request_mock = MagicMock()
        request_mock.user = self.user
        serializer = PatientSerializer(
            resources, many=True, context={"request": request_mock}
        )
        serialized_patients_list = serializer.data

        patient_id_dict = {patient.id: patient for patient in resources}

        matching_patients = [
            (serialized_patient, patient_id_dict[serialized_patient["id"]])
            for serialized_patient in serialized_patients_list
            if serialized_patient["id"] in patient_id_dict
        ]
        alerts = VaccineAlert.get_alerts_by_patient(
            [patient.id for patient in resources]
        )
        for serialized_patient, patient_object in matching_patients:
            parts = []
            patient_name = patient_object.name[0]
            if patient_name.given:
                parts.extend(patient_name.given)
            if patient_name.family:
                parts.append(patient_name.family)
            name = " ".join(parts)

            self.assertEqual(serialized_patient["id"], patient_object.id)
            self.assertEqual(
                serialized_patient["birth_date"],
                patient_object.birthDate.date.strftime("%Y-%m-%d"),
            )
            self.assertEqual(serialized_patient["name"], name)
            self.assertEqual(
                serialized_patient["age_in_days"],
                calculate_age_in_days(
                    patient_object.birthDate.date.strftime("%Y-%m-%d")
                ),
            )
            self.assertEqual(
                serialized_patient["number_of_alerts_by_protocol"], 1
            )  # noqa: E501
            self.assertEqual(
                serialized_patient["alerts"], alerts.get(patient_object.id)
            )
