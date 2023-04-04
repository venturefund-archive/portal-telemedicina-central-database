from datetime import date, datetime

import central_database.integrations.fhir_api.patient as service
import central_database.vaccines.models as vaccine_models


class Patient:
    def __init__(self, id, client=None, query_parameters=None):
        patient_service = service.PatientService(client, query_parameters)
        if id and id != "?":
            self.detail = self._parse_patient_detail(
                patient_service.get_detail(id)
            )  # noqa: E501
        else:
            self.protocol = (
                vaccine_models.VaccineProtocol.get_vaccine_protocol_by_client()
            )
            self.alerts = (
                self.protocol.get_number_of_doses_with_alerts_by_patient()
            )  # noqa: E501
            self.all = self._parse_all(patient_service.get_all(id))

    def _parse_address(self, data):
        if "extension" in data:
            data.pop("extension")
        return {
            "line": data.get("line", None),
            "postal_code": data.get("postalCode", None),
            **data,
        }  # noqa: E501

    def _parse_name(self, data):
        return " ".join(data.get("given")) + " " + data.get("family")

    def _calculate_age_in_days(self, birthdate):
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
        today = date.today()

        age = today - birthdate
        return age.days

    def _parse_patient_detail(self, data):
        return {
            "id": data.get("id", None),
            "name": [
                self._parse_name(name) for name in data.get("name", None)
            ],  # noqa: E501
            "telecom": data.get("telecom"),
            "gender": data.get("gender"),
            "birth_date": data.get("birthDate"),
            "address": [
                self._parse_address(address) for address in data.get("address")
            ],
            "marital_status": data.get("maritalStatus", None),  # noqa: E501
        }

    def _parse_initial_data(self, data):
        return {
            "id": data["id"],
            "number_of_alerts_by_protocol": self.alerts.get(data["id"], 0),
            "name": [
                self._parse_name(name) for name in data.get("name", None)
            ],  # noqa: E501
            "age_in_days": self._calculate_age_in_days(data.get("birthDate")),
        }

    def _parse_all(self, data):
        if data.get("entry", None):
            list_of_patients = [
                self._parse_initial_data(patient.get("resource", None))
                for patient in data.get("entry", None)
            ]
            return list_of_patients
        return []
