import central_database.integrations.fhir_api.patient as service


class Patient:
    def __init__(self, id=None, client=None):
        patient_service = service.PatientService(client)
        if id:
            self.detail = self._parse_patient_detail(
                patient_service.get_detail(id)
            )  # noqa: E501
        else:
            self.all = self._parse_all(patient_service.get_all())

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
            "name": [
                self._parse_name(name) for name in data.get("name", None)
            ],  # noqa: E501
        }

    def _parse_all(self, data):
        if data.get("entry", None):
            list_of_patients = [
                self._parse_initial_data(patient.get("resource", None))
                for patient in data.get("entry", None)
            ]
            return list_of_patients
        return []
