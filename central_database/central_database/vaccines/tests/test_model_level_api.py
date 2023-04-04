import uuid

from rest_framework.test import APITestCase

from central_database.customers.factories import ClientFactory
from central_database.users.tests.factories import UserFactory
from central_database.vaccines.indicators.previne.core import (
    calculate_denominator,
    number_of_patients_with_completed_doses_in_quarter,
)
from central_database.vaccines.tests.factories import (
    VaccineAlertFactory,
    VaccineDoseFactory,
    VaccineProtocolClientFactory,
    VaccineProtocolFactory,
    VaccineStatusFactory,
)


class TestVaccineModelLevelApi(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_it_get_vaccine_alerts_from_vaccine_dose(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1, maximum_recommended_age=2
        )
        vaccine_alert_1 = VaccineAlertFactory(
            vaccine_dose=vaccine_dose, patient_id=1
        )  # noqa: E501
        alert = vaccine_dose.get_vaccine_alerts(1).first()
        self.assertEqual(vaccine_alert_1, alert)

    def test_it_get_vaccine_status_from_vaccine_dose(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1, maximum_recommended_age=2
        )
        vaccine_status = VaccineStatusFactory(
            vaccine_dose=vaccine_dose, patient_id=2
        )  # noqa: E501
        status = vaccine_dose.get_vaccine_status(2).first()
        self.assertEqual(vaccine_status, status)


class TestImmunizationIndicator(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = ClientFactory()

    def test_it_calculates_indicator(self):
        self.vaccine_dose_1 = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        self.vaccine_dose_2 = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        self.protocol = VaccineProtocolFactory(
            vaccine_doses=[self.vaccine_dose_1, self.vaccine_dose_2],
        )
        self.protocol_client = VaccineProtocolClientFactory(
            client=self.client, protocol=self.protocol
        )

        patient_id_list = [str(uuid.uuid4()) for _ in range(100)]
        [
            VaccineStatusFactory(
                vaccine_dose=self.vaccine_dose_1, completed=True, patient_id=patient
            )
            for patient in patient_id_list
        ]

        [
            VaccineStatusFactory(
                vaccine_dose=self.vaccine_dose_2, completed=True, patient_id=patient
            )
            for patient in patient_id_list
        ]

        self.client.ibge_population = 70000
        self.client.sisab_municipal_registration = 50000
        self.client.children_born_alive = 344
        self.client.children_registered_in_APS = 209

        # It simulates the FHIR API Call to get all patients id with twelve months in current quarter
        patients_in_current_quarter = patient_id_list

        patients_with_completed_doses = (
            self.protocol_client._get_patients_with_full_protocol()
        )

        # It will get the intersection between the list of patients id from the FHIR API and the records in database
        numerator = number_of_patients_with_completed_doses_in_quarter(
            patients_in_current_quarter, patients_with_completed_doses
        )
        denominator = calculate_denominator(self.client)

        self.assertEqual(numerator, 100)
        self.assertEqual(denominator, 209)
