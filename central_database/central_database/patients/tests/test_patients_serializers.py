from rest_framework.test import APITestCase

from central_database.patients.api.serializers import PatientSerializer
from central_database.patients.helpers import calculate_age_in_days
from central_database.patients.tests.factories import PatientFactory
from central_database.vaccines.tests.factories import (
    VaccineAlertFactory,
    VaccineAlertTypeFactory,
    VaccineDoseFactory,
    VaccineProtocolFactory,
)


class TestPatientSerializer(APITestCase):
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

        for address_instance, address_data in zip(
            patient.address, serialized_patient["address"]
        ):
            self.assertEqual(address_data["line"], address_instance.line)
            self.assertEqual(address_data["city"], address_instance.city)
            self.assertEqual(address_data["state"], address_instance.state)
            self.assertEqual(
                address_data["postal_code"], address_instance.postalCode
            )  # noqa: E501
            self.assertEqual(address_data["country"], address_instance.country)
            for extension in address_instance.extension[0].extension:
                self.assertEqual(
                    address_data[extension.url], extension.valueDecimal
                )  # noqa: E501
        return serialized_patient

    def test_it_serializes_only_some_fields_for_patient_list(self):

        patient_1 = PatientFactory()
        patient_2 = PatientFactory()
        resources = [patient_1, patient_2]

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
            patient_id=patient_1.id,
            vaccine_dose=self.vaccine_dose_1,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )
        self.vaccine_alert_2 = VaccineAlertFactory(
            patient_id=patient_2.id,
            vaccine_dose=self.vaccine_dose_2,
            alert_type=self.vaccine_alert_type,  # noqa: E501
        )

        self.protocol = VaccineProtocolFactory(
            vaccine_doses=[self.vaccine_dose_1, self.vaccine_dose_2]
        )

        serialized_patients_list = PatientSerializer(resources, many=True).data
        print(serialized_patients_list)
        patient_id_dict = {patient.id: patient for patient in resources}

        matching_patients = [
            (serialized_patient, patient_id_dict[serialized_patient["id"]])
            for serialized_patient in serialized_patients_list
            if serialized_patient["id"] in patient_id_dict
        ]

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
