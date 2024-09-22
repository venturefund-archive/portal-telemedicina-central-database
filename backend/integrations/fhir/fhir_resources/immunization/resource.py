from fhir.resources.R4B.immunization import Immunization as FHIRImmunization
from integrations.fhir.fhir_services.fhir_resource_service import FHIRResourceService
from integrations.fhir.fhir_resources.immunization.builder import FHIRImmunizationBuilder
from typing import List, Dict

class Immunization(FHIRResourceService):
    def __init__(self, client, client_type=None):
        super().__init__(client, client_type)
        self.resource_type = "Immunization"

    def get_all(self) -> List[FHIRImmunization]:
        search_params = {}
        results = self.client.search_resources(self.resource_type, search_params)
        return [FHIRImmunization.parse_obj(resource) for resource in results.get('entry', [])]

    def get_patient_immunizations(self, patient_id: str) -> List[FHIRImmunization]:
        search_params = {"patient": f"Patient/{patient_id}"}
        results = self.client.search_resources(self.resource_type, search_params)
        return [FHIRImmunization.construct(**resource['resource']) for resource in results.get('entry', [])]

    def create(self, data: Dict) -> FHIRImmunization:
        immunization = FHIRImmunizationBuilder.build(data)
        created_resource = self.client.create_resource(self.resource_type, immunization.dict())
        return FHIRImmunization.parse_obj(created_resource)

    @staticmethod
    def filter_individual_data(immunization: FHIRImmunization) -> dict:
        return {
            "id": immunization.id,
            "status": immunization.status,
            "occurrence_date": immunization.occurrenceDateTime if immunization.occurrenceDateTime else None,
            "recommendation": {
                "patient_id": immunization.patient.get('reference', None),
                "vaccine_dose": {
                    "dose_order": immunization.protocolApplied[0].get('doseNumberString', None),
                    "vaccine": {
                        "code": immunization.vaccineCode.get('coding', [{}])[0].get('code', None) if immunization.vaccineCode else None,
                        "display": immunization.vaccineCode.get('coding', [{}])[0].get('display', None) if immunization.vaccineCode else None,
                        "system": immunization.vaccineCode.get('coding', [{}])[0].get('system', None) if immunization.vaccineCode else None,
                    }
                }
            }
        }

    @staticmethod
    def filter_data(immunizations: List[FHIRImmunization]) -> List[dict]:
        return [Immunization.filter_individual_data(immunization) for immunization in immunizations]