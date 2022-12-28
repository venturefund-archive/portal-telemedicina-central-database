import google.auth
import requests
from django.conf import settings
from google.auth.transport import requests as google_requests

# from google.oauth2 import service_account

fhir_url = f"http://{settings.FHIR_API_HOST}:{settings.FHIR_API_PORT}/fhir/"


def get_resource(resource_type, resource_id=None, client=None):
    if settings.USE_HEALTHCARE_API:
        return get_resource_from_healthcare_api(
            resource_type, resource_id, client
        )  # E501: noqa
    return get_resource_from_default_fhir_store(resource_type, resource_id)


def get_resource_from_healthcare_api(resource_type, resource_id, client):
    project_id = settings.HEALTHCARE_API_PROJECT_ID
    location = settings.HEALTHCARE_API_PROJECT_LOCATION
    dataset_id = client.dataset_id
    fhir_store_id = client.fhir_store_id

    # credentials = service_account.Credentials.from_service_account_file(
    #     f"{settings.CENTRAL_DATABASE_PATH}/integrations/fhir_api/credentials.json"
    # )

    credentials, _ = google.auth.default()

    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )

    session = google_requests.AuthorizedSession(scoped_credentials)

    base_url = "https://healthcare.googleapis.com/v1"
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/{}/".format(
        url, dataset_id, fhir_store_id, resource_type
    )

    if resource_id:
        resource_path = resource_path + f"{resource_id}"

    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    response = session.get(resource_path, headers=headers)
    response.raise_for_status()

    resource = response.json()
    return resource


def get_resource_from_default_fhir_store(resource_type, resource_id):
    url = fhir_url + resource_type
    if resource_id:
        url = url + f"/{resource_id}"
    data = requests.get(url)
    return data.json()
