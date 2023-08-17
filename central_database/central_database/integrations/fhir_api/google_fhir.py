import google.auth
from fhirclient.client import FHIRClient
from fhirclient.models.bundle import Bundle
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


def default_save_func(x):
    return x


class GoogleFHIRClient(FHIRClient):
    def __init__(self, settings=None, state=None, save_func=default_save_func):
        super().__init__(settings=settings, state=state, save_func=save_func)
        self.server = GoogleFHIRServer(
            self, base_uri=settings["api_base"], custom_session=True
        )

    def fetch_all_pages(self, search):
        bundle = search.perform(self.server)

        all_bundles = []

        while bundle is not None:
            all_bundles.append(bundle)
            next_link = None
            for link in bundle.link:
                if link.relation == "next":
                    next_link = link.url
                    break

            if next_link:
                bundle = Bundle.read_from(next_link, self.server)
            else:
                bundle = None
        return all_bundles


def server_settings(dataset, fhirstore):
    return {
        "app_id": "di_app",
        "api_base": f"https://healthcare.googleapis.com/v1/projects/ptm-gestao-di-dev/locations/southamerica-east1/datasets/{dataset}/fhirStores/{fhirstore}/fhir",  # noqa: E501
    }
