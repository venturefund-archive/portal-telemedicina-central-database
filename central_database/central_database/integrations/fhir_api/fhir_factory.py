from fhirclient import client

from .google_fhir import GoogleFHIRClient


def create_fhir_client(client_type="default"):
    if client_type == "google":
        return GoogleFHIRClient(settings={})
    elif client_type == "default":
        # Replace with your FHIR server URL
        return client.FHIRClient(
            settings={
                "app_id": "my_fhir_app",
                "api_base": "https://fhir.example.com",
            }  # E501: noqa
        )
    else:
        raise ValueError(f"Invalid client_type: {client_type}")
