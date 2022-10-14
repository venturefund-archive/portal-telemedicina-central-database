import requests


class PatientService():

    def __init__(self):
        self.url = "http://172.18.0.6:8080/fhir/"

    def get_all(self):
        url = self.url + 'Patient'
        return requests.get(url).json()

    def get_detail(self, id):
        url = self.url + 'Patient' + f'/{id}'
        return requests.get(url).json()

    def get_immunization(self, id):
        url = self.url + f"/Immunization?patient={id}"
        return requests.get(url).json()
