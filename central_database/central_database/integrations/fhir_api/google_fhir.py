import google.auth
from fhirclient.client import FHIRClient
from fhirclient.server import FHIRServer
from google.auth.transport import requests as google_requests


class GoogleFHIRServer(FHIRServer):
    def __init__(self, client, base_uri=None, state=None, custom_session=None):
        super().__init__(client, base_uri, state)

        if custom_session is not None:
            credentials, _ = google.auth.default()

            scoped_credentials = credentials.with_scopes(
                ["https://www.googleapis.com/auth/cloud-platform"]
            )

            session = google_requests.AuthorizedSession(scoped_credentials)
            self.session = session


class GoogleFHIRClient(FHIRClient):
    def __init__(self, settings=None, state=None, save_func=lambda x: x):
        super().__init__(settings=settings, state=state, save_func=save_func)
        self.server = GoogleFHIRServer(
            self, base_uri=settings["api_base"], custom_session=True
        )

    def fetch_page(self, search):
        bundle = search.perform(self.server)
        next_link = None
        for link in bundle.link:
            if link.relation == "next":
                next_link = link.url
                break

        return bundle, next_link


def server_settings(dataset, fhirstore):
    return {
        "app_id": "di_app",
        "api_base": f"https://healthcare.googleapis.com/v1/projects/ptm-gestao-di-dev/locations/southamerica-east1/datasets/{dataset}/fhirStores/{fhirstore}/fhir",  # noqa: E501
    }
