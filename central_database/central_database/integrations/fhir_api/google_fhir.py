import json

from fhirclient import client
from google.auth.transport import requests as google_requests
from google.oauth2 import service_account


class GoogleFHIRClient(client.FHIRClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load Google Healthcare API settings from Django settings
        from django.conf import settings

        self.project_id = settings.HEALTHCARE_API_PROJECT_ID
        self.location = settings.HEALTHCARE_API_PROJECT_LOCATION
        self.dataset_id = settings.HEALTHCARE_API_DATASET_ID
        self.fhir_store_id = settings.HEALTHCARE_API_FHIR_STORE_ID
        credentials_path = f"{settings.CENTRAL_DATABASE_PATH}/integrations/fhir_api/credentials.json"  # noqa: E501

        # Set up Google API credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        # credentials, _ = google.auth.default()
        scoped_credentials = credentials.with_scopes(
            ["https://www.googleapis.com/auth/cloud-platform"]
        )
        self.session = google_requests.AuthorizedSession(scoped_credentials)

    def request_json(self, path, nosign=False):
        full_url = self.construct_resource_url(path)

        headers = {
            "Content-Type": "application/fhir+json;charset=utf-8",
            "Accept": "application/fhir+json",
        }

        response = self.session.get(full_url, headers=headers)
        response.raise_for_status()
        return json.loads(response.text)

    def construct_resource_url(self, path):
        base_url = "https://healthcare.googleapis.com/v1"
        url = f"{base_url}/projects/{self.project_id}/locations/{self.location}"  # noqa: E501
        resource_path = f"{url}/datasets/{self.dataset_id}/fhirStores/{self.fhir_store_id}/fhir/{path}"  # noqa: E501
        return resource_path
