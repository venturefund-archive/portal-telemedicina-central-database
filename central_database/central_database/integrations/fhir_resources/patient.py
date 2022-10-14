from central_database.integrations.fhir_api.patient import PatientService


class PatientDetail():
    def __init__(self, id):
        service = PatientService()
        self.detail = self.parse_patient_detail(service.get_detail(id))

    def parse_address(self, data):
        data.pop("extension")
        return {
            "line": data["line"][0],
            "postal_code": data["postalCode"],
            **data
        }

    def parse_patient_detail(self, data):
        return {
            "id": data["id"],
            "name": data["name"][0]["family"],
            "phone": data["telecom"][0]["value"],
            "gender": data["gender"],
            "birth_date": data["birthDate"],
            "address": self.parse_address(data["address"][0]),
            "marital_status": data["maritalStatus"]["text"]
        }


class PatientImmunization():
    def __init__(self, id):
        service = PatientService()
        self.immunization = self.parse_patient_immunization(
            service.get_immunization(id)
        )

    def parse_vaccine(self, data):
        coding = data.pop("coding")[0]
        return {
            **coding,
            **data
        }

    def parse_immunization(self, data):
        return {
            "id": data["id"],
            "vaccine": self.parse_vaccine(data["vaccineCode"]),
            "status": data["status"],
            "timestamp": data["occurrenceDateTime"]
        }

    def parse_patient_immunization(self, data):
        immunizations = data["entry"]
        immunizations_list = [
            self.parse_immunization(immunization["resource"])
            for immunization in immunizations
        ]
        return immunizations_list
