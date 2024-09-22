from fhir.resources.R4B.immunizationrecommendation import ImmunizationRecommendation as FHIRImmunizationRecommendation
from integrations.fhir.fhir_services.fhir_resource_service import FHIRResourceService
from typing import List, Dict
from integrations.fhir.fhir_resources.immunization_recommendation.builder import FHIRImmunizationRecommendationBuilder


class ImmunizationRecommendation(FHIRResourceService):
    def __init__(self, client, client_type=None):
        super().__init__(client, client_type)
        self.resource_type = "ImmunizationRecommendation"

    def get_all(self) -> List[FHIRImmunizationRecommendation]:
        search_params = {}
        results = self.client.search_resources(self.resource_type, search_params)
        return [FHIRImmunizationRecommendation.parse_obj(resource) for resource in results.get('entry', [])]

    def get_patient_immunization_recommendations(self, patient_id: str) -> List[FHIRImmunizationRecommendation]:
        search_params = {"patient": f"Patient/{patient_id}"}
        results = self.client.search_resources(self.resource_type, search_params)
        return [FHIRImmunizationRecommendation.construct(**resource['resource']) for resource in results.get('entry', [])]

    def create(self, data: Dict) -> FHIRImmunizationRecommendation:
        recommendation = FHIRImmunizationRecommendationBuilder.build(data)
        created_resource = self.client.create_resource(self.resource_type, recommendation.dict())
        return FHIRImmunizationRecommendation.parse_obj(created_resource)
    
    def update(self, data: Dict) -> FHIRImmunizationRecommendation:
        recommendation = self.client.get_resource(self.resource_type, data['id'])
        recommendation = FHIRImmunizationRecommendation.parse_obj(recommendation)
        recommendation.recommendation[0].forecastStatus.coding[0].code = data['forecast_status']
        updated_resource = self.client.update_resource(self.resource_type, recommendation.dict())
        return FHIRImmunizationRecommendation.parse_obj(updated_resource)

    @staticmethod
    def filter_individual_data(recommendation: FHIRImmunizationRecommendation) -> dict:
        recommendation_data = recommendation.recommendation[0]
        vaccine_code = recommendation_data.get('vaccineCode', {})[0].get('coding', [{}])[0]
        return {
            "id": recommendation.id,
            "patient_id": recommendation.patient.get('reference', None),
            "due_date": recommendation_data.get('dateCriterion', [{}])[0].get('value', None),
            "forecast_status": recommendation_data.get('forecastStatus', {}).get('coding', [{}])[0].get('code', None) if recommendation_data.get('forecastStatus') else None,
            "vaccine_dose": {
                "dose_order": recommendation_data.get('seriesDosesPositiveInt', None),
                "vaccine": vaccine_code
            },
        }

    @staticmethod
    def filter_data(recommendations: List[FHIRImmunizationRecommendation]) -> dict:
        return [ImmunizationRecommendation.filter_individual_data(recommendation) for recommendation in recommendations]