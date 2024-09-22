from django.conf import settings
from rest_framework.viewsets import GenericViewSet

class FHIRBaseViewSet(GenericViewSet):
    fhir_resource_class = None

    def _handle_fhir_operation(self, operation, *args, **kwargs):
        if settings.USE_FHIR_STORE:
            client = self.request.user.client
            fhir_resource = self.fhir_resource_class(client)
            result = getattr(fhir_resource, operation)(*args, **kwargs)
            return self.fhir_resource_class.filter_data(result)
        else:
            return None

    def get_queryset(self):
        if settings.USE_FHIR_STORE:
            return None
        return super().get_queryset()
    