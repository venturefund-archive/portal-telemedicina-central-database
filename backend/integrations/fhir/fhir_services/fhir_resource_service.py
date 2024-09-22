from integrations.fhir.fhir_services.client.fhir_api_client_factory import FHIRAPIClientFactory


class FHIRResourceService:
    _client = None

    def __init__(self, client, client_type=None):
        if not FHIRResourceService._client:
            FHIRResourceService._client = self.initialize_client(client, client_type)
        self.client = FHIRResourceService._client

    def initialize_client(self, client, client_type):
        return FHIRAPIClientFactory.get_client(
            client_type=client_type,
            dataset_id=client.fhir_store.dataset.dataset_id,
            fhir_store_id=client.fhir_store.fhir_store_id
        )
