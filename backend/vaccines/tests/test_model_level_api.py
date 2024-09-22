from rest_framework.test import APITestCase

from users.tests.factories import UserFactory
from vaccines.tests.factories import (
    VaccineAlertFactory,
    VaccineDoseFactory,
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
