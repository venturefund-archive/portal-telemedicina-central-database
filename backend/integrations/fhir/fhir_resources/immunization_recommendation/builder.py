from fhir.resources.R4B.immunizationrecommendation import ImmunizationRecommendation as FHIRImmunizationRecommendation
from fhir.resources.R4B.reference import Reference
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.coding import Coding
from typing import Dict

class FHIRImmunizationRecommendationBuilder:
    @staticmethod
    def build(data: Dict) -> FHIRImmunizationRecommendation:
        return FHIRImmunizationRecommendation(
            patient=Reference(reference=f"Patient/{data['patient_id']}"),
            date=data['date'].isoformat(),
            recommendation=[{
                "vaccineCode": CodeableConcept(
                    coding=[Coding(
                        system=data.get('vaccine_system', "https://integracao.esusab.ufsc.br/ledi/documentacao/referencias/dicionario.html#imunobiologico"),
                        code=str(data['vaccine_dose'].vaccine.code),
                        display=data['vaccine_dose'].vaccine.display
                    )]
                ),
                "forecastStatus": CodeableConcept(
                    coding=[Coding(
                        system="http://terminology.hl7.org/CodeSystem/immunization-recommendation-status",
                        code=data['forecast_status'],
                        display=data['forecast_status'].capitalize()
                    )]
                ),
                "dateCriterion": [{
                    "code": CodeableConcept(
                        coding=[Coding(
                            system="http://loinc.org",
                            code="30980-7",
                            display="Date vaccine due"
                        )]
                    ),
                    "value": data['due_date'].isoformat()
                }],
                "doseNumberPositiveInt": data['vaccine_dose'].dose_order,
                "seriesDosesPositiveInt": data['vaccine_dose'].vaccine.doses.count()
            }]
        )
