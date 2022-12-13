from central_database.integrations.fhir_api.immunization import (  # noqa: E501
    ImmunizationService,
)


class Immunization:
    def __init__(self, id=None):
        service = ImmunizationService()
        if id:
            self.patient_immunization = self._parse_patient_immunization(
                service.get_patient_immunization(id)
            )
        else:
            self.all = self._parse_all(service.get_all())

    def _parse_vaccine(self, data):
        coding = data.pop("coding")[0]
        return {**coding, **data}

    def _parse_immunization(self, data):
        return {
            "id": data.get("id", None),
            "vaccine": self._parse_vaccine(data.get("vaccineCode", None)),
            "status": data.get("status", None),
            "timestamp": data.get("occurrenceDateTime", None),
        }

    def _parse_patient_immunization(self, data):
        immunizations = data.get("entry")
        immunizations_list = [
            self._parse_immunization(immunization.get("resource", None))
            for immunization in immunizations
        ]
        return immunizations_list

    def _parse_patient_id(self, data):
        patient = data.get("patient", None)
        if patient:
            patient_reference = patient.get("reference", None)
            patient = int(patient_reference[8:])
        return patient

    def _parse_all(self, data):
        immunizations = data.get("entry", None)
        immunizations_list = [
            {
                "patient_id": self._parse_patient_id(
                    immunization.get("resource", None)
                ),
                **self._parse_immunization(immunization.get("resource", None)),
            }
            for immunization in immunizations
        ]
        return immunizations_list
