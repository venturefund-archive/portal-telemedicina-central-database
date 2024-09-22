from django.conf import settings
from integrations.fhir.fhir_services.client.fhir_api_client import FHIRAPIClient
from integrations.fhir.fhir_services.client.setup.fhir_api_setup import GoogleFHIRAPISetup

class FHIRAPIClientFactory:
    @staticmethod
    def get_client(client_type: str = None, **kwargs):
        client_type = client_type or settings.DEFAULT_FHIR_CLIENT
        
        if client_type == 'google':
            setup = GoogleFHIRAPISetup(
                project_id=kwargs.get('project_id') or settings.FHIR_PROJECT_ID,
                location=kwargs.get('location') or settings.FHIR_LOCATION,
                dataset_id=kwargs.get('dataset_id'),
                fhir_store_id=kwargs.get('fhir_store_id')
            )
            return FHIRAPIClient(setup)
        else:
            raise ValueError(f"Unsupported FHIR client type: {client_type}")
