from fhir.resources.R4B.immunization import Immunization
from fhir.resources.R4B.reference import Reference
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.coding import Coding
from typing import Dict
from datetime import datetime


class FHIRImmunizationBuilder:
    @staticmethod
    def build(data: Dict) -> Immunization:
        occurrence_date = datetime.strptime(data['occurrence_date'], '%Y-%m-%d').date() if 'occurrence_date' in data else None
        return Immunization(
            status=data['status'],
            patient=Reference(reference=f"Patient/{data['recommendation']['patient_id']}"),
            occurrenceDateTime=occurrence_date,
            vaccineCode=CodeableConcept(
                coding=[Coding(
                    system="https://integracao.esusab.ufsc.br/ledi/documentacao/referencias/dicionario.html#imunobiologico",
                    code=str(data['recommendation']['vaccine_dose']['vaccine']['code']),
                    display=data['recommendation']['vaccine_dose']['vaccine']['display']
                )]
            ),
            primarySource=data['primary_source'],
            performer=[{
                "actor": Reference(reference=f"Practitioner/{data['performer']['id']}")
            }] if 'performer' in data else None
        )
