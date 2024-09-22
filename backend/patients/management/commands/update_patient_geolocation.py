from django.core.management.base import BaseCommand
from patients.geo_coder import GeocodeFetcher
from django.conf import settings
from integrations.fhir.fhir_resources.patient import Patient as FHIRPatient
from fhir.resources.R4B.extension import Extension
from fhir.resources.R4B.patient import Patient
from customers.models import Client


class Command(BaseCommand):
    help = 'Update patient geolocation data in FHIR'

    def add_arguments(self, parser):
        parser.add_argument('client_name', type=str, help='Client name')

    def handle(self, *args, **options):
        geocode_fetcher = GeocodeFetcher(settings.GOOGLE_MAPS_API_KEY)

        client_name = options["client_name"]
        client = Client.objects.get(client_name=client_name)

        fhir_client = FHIRPatient(client=client, client_type='google')
        # Fetch all patients from FHIR
        fhir_patients = fhir_client.get_all_pages_resources()

        for fhir_patient in fhir_patients:
            if fhir_patient.address:
                # Check if the address already has a geolocation extension
                if any(ext.get('url') == "http://hl7.org/fhir/StructureDefinition/geolocation" 
                       for ext in fhir_patient.address[0].get('extension', [])):
                    self.stdout.write(self.style.SUCCESS(f"Patient {fhir_patient.id} already has geolocation. Skipping."))
                    continue
                

                # Check if address is empty
                if not fhir_patient.address[0].get('line') and not fhir_patient.address[0].get('city') and not fhir_patient.address[0].get('state') and not fhir_patient.address[0].get('postalCode') and not fhir_patient.address[0].get('country'):
                    # Coordinates for the center of COCAL PIAUI
                    lat, lng = -3.4731, -41.5572
                    self.stdout.write(self.style.WARNING(f"Empty address for patient {fhir_patient.id}. Using COCAL PIAUI coordinates."))
                else:
                    address = self.format_address(fhir_patient.address[0])
                    lat, lng = geocode_fetcher.get_geocode(address)

                if lat is not None and lng is not None:
                    # Update FHIR resource
                    geolocation_extension = Extension(
                        url="http://hl7.org/fhir/StructureDefinition/geolocation",
                        extension=[
                            Extension(url="latitude", valueDecimal=str(lat)),
                            Extension(url="longitude", valueDecimal=str(lng))
                        ]
                    )

                    # Update the address with new geolocation
                    fhir_patient.address[0]['extension'] = [geolocation_extension]

                    # Update the FHIR resource
                    updated_fhir_patient = fhir_client.update_patient(fhir_patient)
                    if updated_fhir_patient:
                        self.stdout.write(self.style.SUCCESS(f"Updated geolocation for patient {fhir_patient.id} in FHIR"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Failed to update FHIR resource for patient {fhir_patient.id}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Could not geocode address for patient {fhir_patient.id}"))
            else:
                self.stdout.write(self.style.WARNING(f"No address found for patient {fhir_patient.id}"))

        self.stdout.write(self.style.SUCCESS("Geolocation update completed"))

    def format_address(self, address):
        address_parts = [
            ', '.join(address.get('line', [])),
            address.get('city'),
            address.get('state'),
            address.get('postalCode'),
            address.get('country')
        ]
        return ', '.join(filter(None, address_parts))