from integrations.fhir.fhir_services.client.setup.base.fhir_api_setup import FHIRAPISetup
from google.auth.transport.requests import AuthorizedSession
from google.auth import default

class GoogleFHIRAPISetup(FHIRAPISetup):
    def __init__(self, project_id: str, location: str, dataset_id: str, fhir_store_id: str):
        self.project_id = project_id
        self.location = location
        self.dataset_id = dataset_id
        self.fhir_store_id = fhir_store_id

    def get_base_url(self) -> str:
        return f"https://healthcare.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/datasets/{self.dataset_id}/fhirStores/{self.fhir_store_id}/fhir"

    def get_session(self):
        credentials, _ = default()
        return AuthorizedSession(credentials)
