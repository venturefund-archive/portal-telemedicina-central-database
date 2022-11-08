from rest_framework.test import APITestCase

from central_database.users.tests.factories import UserFactory
from central_database.vaccines.tests.factories import (
    VaccineAlertFactory,
    VaccineDoseFactory,
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
