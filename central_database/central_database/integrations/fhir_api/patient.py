import requests

from central_database.integrations.fhir_api.schema import fhir_url


class PatientService:
    def __init__(self):
        self.url = fhir_url

    def get_all(self):
        url = self.url + "Patient"
        data = requests.get(url)
        return data.json()

    def get_detail(self, id):
        url = self.url + "Patient" + f"/{id}"
        data = requests.get(url)
        return data.json()
