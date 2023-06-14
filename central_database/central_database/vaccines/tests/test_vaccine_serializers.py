from datetime import datetime

from dateutil.relativedelta import relativedelta
from rest_framework.test import APITestCase

from central_database.vaccines.api.serializers import (
    VaccineDosesSerializer,
    VaccineProtocolSerializer,
    VaccineSerializer,
    VaccineStatusSerializer,
)
from central_database.vaccines.tests.factories import (  # noqa: E501
    VaccineAlertFactory,
    VaccineAlertTypeFactory,
    VaccineDoseFactory,
    VaccineFactory,
    VaccineProtocolFactory,
    VaccineStatusFactory,
)


class TestVaccineDoseSerializer(APITestCase):
    def test_it_serializes_vaccine(self):
        vaccine = VaccineFactory()

        serialized_vaccine = VaccineSerializer(vaccine).data

        self.assertEqual(serialized_vaccine["id"], vaccine.id),
        self.assertEqual(serialized_vaccine["system"], vaccine.system),
        self.assertEqual(serialized_vaccine["code"], vaccine.code),
        self.assertEqual(serialized_vaccine["display"], vaccine.display),
        self.assertEqual(
            serialized_vaccine["description"], vaccine.description
        )  # noqa: E501

    def test_it_serializes_vaccine_doses(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1, maximum_recommended_age=2
        )
        vaccine_dose.active_alerts = []
        vaccine_dose.patient_status = []
        serialized_vaccine_dose = VaccineDosesSerializer(vaccine_dose).data

        self.assertEqual(
            serialized_vaccine_dose["vaccine"],
            vaccine_dose.vaccine.id,
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_dose["minimum_recommended_age"],
            vaccine_dose.minimum_recommended_age,
        )
        self.assertEqual(
            serialized_vaccine_dose["maximum_recommended_age"],
            vaccine_dose.maximum_recommended_age,
        )
        self.assertEqual(
            serialized_vaccine_dose["dose_order"], vaccine_dose.dose_order
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_dose["gender_recommendation"],
            vaccine_dose.gender_recommendation,
        )

    def test_it_serializes_vaccine_doses_with_alerts(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1, maximum_recommended_age=2
        )
        alert = VaccineAlertFactory(vaccine_dose=vaccine_dose, patient_id=11)
        vaccine_dose.active_alerts = [alert]
        vaccine_dose.patient_status = []
        VaccineDosesSerializer.context = {"patient_id": 11}
        serialized_vaccine_dose = VaccineDosesSerializer(vaccine_dose).data
        self.assertEqual(
            serialized_vaccine_dose["vaccine"],
            vaccine_dose.vaccine.id,
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_dose["minimum_recommended_age"],
            vaccine_dose.minimum_recommended_age,
        )
        self.assertEqual(
            serialized_vaccine_dose["maximum_recommended_age"],
            vaccine_dose.maximum_recommended_age,
        )
        self.assertEqual(
            serialized_vaccine_dose["dose_order"], vaccine_dose.dose_order
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_dose["gender_recommendation"],
            vaccine_dose.gender_recommendation,
        )
        self.assertEqual(serialized_vaccine_dose["alerts"][0]["id"], alert.id)
        self.assertEqual(
            serialized_vaccine_dose["alerts"][0]["patient_id"],
            alert.patient_id,  # noqa: E501
        )

        self.assertEqual(
            serialized_vaccine_dose["alerts"][0]["created_at"],
            alert.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
        self.assertEqual(
            serialized_vaccine_dose["alerts"][0]["active"], alert.active
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_dose["alerts"][0]["vaccine_dose"],
            alert.vaccine_dose.id,  # noqa: E501
        )
        self.assertEqual(
            serialized_vaccine_dose["alerts"][0]["alert_type"],
            alert.alert_type.id,  # noqa: E501
        )

    def test_it_serializes_vaccine_doses_with_status(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1, maximum_recommended_age=2
        )
        status = VaccineStatusFactory(
            vaccine_dose=vaccine_dose,
            completed=True,
            application_date=datetime.now(),  # noqa: E501
        )
        vaccine_dose.active_alerts = []
        vaccine_dose.patient_status = [status]
        VaccineDosesSerializer.context = {"patient_id": 11}
        serialized_vaccine_dose = VaccineDosesSerializer(vaccine_dose).data
        self.assertEqual(
            serialized_vaccine_dose["vaccine"],
            vaccine_dose.vaccine.id,
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_dose["minimum_recommended_age"],
            vaccine_dose.minimum_recommended_age,
        )
        self.assertEqual(
            serialized_vaccine_dose["maximum_recommended_age"],
            vaccine_dose.maximum_recommended_age,
        )
        self.assertEqual(
            serialized_vaccine_dose["dose_order"], vaccine_dose.dose_order
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_dose["gender_recommendation"],
            vaccine_dose.gender_recommendation,
        )
        self.assertEqual(
            serialized_vaccine_dose["status"]["completed"], status.completed
        )
        self.assertEqual(
            serialized_vaccine_dose["status"]["application_date"],
            status.application_date.strftime("%Y-%m-%d"),
        )


class TestVaccineProtocolSerializer(APITestCase):
    def test_it_serializes_vaccine_protocol_with_metrics(self):
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

        serialized_vaccine_protocol = VaccineProtocolSerializer(
            self.protocol
        ).data  # noqa: E501

        self.assertEqual(
            serialized_vaccine_protocol["vaccine_doses"],
            [
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
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_protocol["completed_doses_count"], 0
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_protocol["completed_doses_percentage"], 0
        )  # noqa: E501
        self.assertEqual(serialized_vaccine_protocol["alert_doses_count"], 3)
        self.assertEqual(
            serialized_vaccine_protocol["expected_doses_count"], 3
        )  # noqa: E501


class TestVaccineStatusSerializer(APITestCase):
    def test_it_serializes_vaccine_status(self):
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        date_now = datetime.now()
        vaccine_status = VaccineStatusFactory(
            vaccine_dose=vaccine_dose,
            application_date=date_now,
            next_dose_application_date=date_now + relativedelta(months=+1),
            health_professional=None,
        )

        serialized_vaccine_status = VaccineStatusSerializer(
            vaccine_status
        ).data  # noqa: E501

        self.assertEqual(serialized_vaccine_status["id"], vaccine_status.id)
        self.assertEqual(
            serialized_vaccine_status["health_professional"],
            vaccine_status.health_professional,
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["batch"], vaccine_status.batch
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["patient_id"], vaccine_status.patient_id
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["completed"], vaccine_status.completed
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["application_date"],
            vaccine_status.application_date.strftime("%Y-%m-%d"),
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["next_dose_application_date"],
            vaccine_status.next_dose_application_date.strftime("%Y-%m-%d"),
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["vaccine_dose"],
            vaccine_status.vaccine_dose.id,  # noqa: E501
        )

    def test_it_serializes_vaccines_status_with_nested_health_professional(
        self,
    ):  # noqa: E501
        vaccine_dose = VaccineDoseFactory(
            minimum_recommended_age=1,
            maximum_recommended_age=2,
        )
        date_now = datetime.now()

        vaccine_status = VaccineStatusFactory(
            vaccine_dose=vaccine_dose,
            application_date=date_now,
            next_dose_application_date=date_now + relativedelta(months=+1),
        )

        serialized_vaccine_status = VaccineStatusSerializer(
            vaccine_status
        ).data  # noqa: E501

        self.assertEqual(serialized_vaccine_status["id"], vaccine_status.id)
        self.assertEqual(
            serialized_vaccine_status["health_professional"]["id"],
            vaccine_status.health_professional.id,
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["health_professional"]["name"],
            vaccine_status.health_professional.name,
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["health_professional"]["cns_number"],
            vaccine_status.health_professional.cns_number,
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["health_professional"]["cnes_number"],
            vaccine_status.health_professional.cnes_number,
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["health_professional"]["client"],
            vaccine_status.health_professional.client.id,
        )  # noqa: E501

        self.assertEqual(
            serialized_vaccine_status["batch"], vaccine_status.batch
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["patient_id"], vaccine_status.patient_id
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["completed"], vaccine_status.completed
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["application_date"],
            vaccine_status.application_date.strftime("%Y-%m-%d"),
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["next_dose_application_date"],
            vaccine_status.next_dose_application_date.strftime("%Y-%m-%d"),
        )  # noqa: E501
        self.assertEqual(
            serialized_vaccine_status["vaccine_dose"],
            vaccine_status.vaccine_dose.id,  # noqa: E501
        )
