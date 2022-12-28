from central_database.integrations.fhir_api.schema import get_resource


class PatientService:
    def __init__(self, client):
        self.resource_type = "Patient"
        self.client = client

    def get_all(self):
        return get_resource(self.resource_type, client=self.client)

    def get_detail(self, id):
        return get_resource(self.resource_type, id, client=self.client)
