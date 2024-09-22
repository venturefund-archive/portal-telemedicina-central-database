from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.humanname import HumanName
from fhir.resources.R4B.contactpoint import ContactPoint
from fhir.resources.R4B.address import Address
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.identifier import Identifier
from typing import Dict
from datetime import datetime


class FHIRPatientBuilder:
    @staticmethod
    def build(data: Dict) -> Patient:
        birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date() if 'birth_date' in data else None
        patient = Patient(
            id=data.get('id'),
            birthDate=birth_date,
            gender=data.get('gender'),
            maritalStatus=CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",
                    code=data['marital_status'],
                    display=data['marital_status'].capitalize()
                )]
            ) if 'marital_status' in data else None

        )

        if 'name' in data:
            patient.name = [HumanName(
                text=data['name']
            )]

        if 'telecom' in data:
            patient.telecom = [ContactPoint(
                system="phone",
                value=data['telecom'],
                use="home"
            )]

        if 'address' in data:
            address_data = data['address']
            patient.address = [Address(
                line=address_data.get('line', ['']),
                city=address_data.get('city'),
                state=address_data.get('state'),
                postalCode=address_data.get('postal_code'),
                country=address_data.get('country'),
                district=address_data.get('district')
            )]

        if "identifier" in data:
            patient.identifier = patient.identifier or []
            for identifier in data["identifier"]:
                    patient.identifier.append(Identifier(
                        system=identifier["system"],
                        value=identifier["value"],
                        use=identifier["use"]
                    ))
        # if 'identifier_cpf' in data:
        #     patient.identifier = patient.identifier or []
        #     patient.identifier.append(Identifier(
        #         system="http://rnds.saude.gov.br/fhir/r4/NamingSystem/cpf",
        #         value=data['identifier_cpf']
        #     ))

        # if 'identifier_cns' in data:
        #     patient.identifier = patient.identifier or []
        #     patient.identifier.append(Identifier(
        #         system="http://rnds.saude.gov.br/fhir/r4/NamingSystem/cns",
        #         value=data['identifier_cns']
        #     ))

        return patient
