from central_database.integrations.fhir_api.schema import get_resource


class PatientService:
    def __init__(self, client, query_parameters):
        self.resource_type = "Patient"
        self.client = client
        self.query_parameters = query_parameters

    def get_all(self, id):
        return get_resource(
            self.resource_type,
            id,
            client=self.client,
            query_parameters=self.query_parameters,
        )

    def get_detail(self, id):
        return get_resource(self.resource_type, id, client=self.client)
