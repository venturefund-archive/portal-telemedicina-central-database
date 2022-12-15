from django.conf import settings

fhir_url = f"http://{settings.FHIR_API_HOST}:{settings.FHIR_API_PORT}/fhir/"
