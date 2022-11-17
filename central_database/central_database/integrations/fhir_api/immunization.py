import requests

from central_database.integrations.fhir_api.schema import fhir_url


class ImmunizationService:
    def __init__(self):
        self.url = fhir_url

    def get_all(self):
        url = self.url + "Immunization"
        return requests.get(url).json()

    def get_patient_immunization(self, id):
        url = self.url + f"/Immunization?patient={id}"
        return requests.get(url).json()
