from django.conf import settings
from fhirclient.client import FHIRClient
from fhirclient.server import FHIRServer
from google.auth.transport import requests as google_requests
from google.oauth2 import service_account


class GoogleFHIRServer(FHIRServer):
    def __init__(self, client, base_uri=None, state=None, custom_session=None):
        # Call the parent constructor
        super().__init__(client, base_uri, state)

        if custom_session is not None:
            credentials = service_account.Credentials.from_service_account_file(  # noqa: E501
                f"{settings.CENTRAL_DATABASE_PATH}/integrations/fhir_api/credentials.json"  # noqa: E501
            )

            # credentials, _ = google.auth.default()

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


# settings = {
# 'app_id': 'my_web_app',
# 'api_base': 'https://healthcare.googleapis.com/v1/projects/ptm-gestao-di-dev/locations/southamerica-east1/datasets/taruma_data/fhirStores/taruma_dev_immunization/fhir'  # noqa: E501

# }
