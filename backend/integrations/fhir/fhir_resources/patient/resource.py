from datetime import date, datetime
from integrations.fhir.fhir_services.fhir_resource_service import FHIRResourceService
from fhir.resources.R4B.patient import Patient as FHIRPatient
from .builder import FHIRPatientBuilder
from typing import List, Dict, Any

class Patient(FHIRResourceService):
    def __init__(self, client, client_type=None):
        super().__init__(client, client_type)
        self.resource_type = "Patient"

    def get_all(self, params=None) -> List[FHIRPatient]:
        results = self.client.search_resources(self.resource_type, params)
        return [FHIRPatient.construct(**resource['resource']) for resource in results.get('entry', [])]
    
    def get_all_pages_resources(self, params=None) -> List[FHIRPatient]:
        results = self.client.fetch_all_pages_resources(self.resource_type, params)
        return [FHIRPatient.construct(**result) for result in results]

    def get_patient_by_id(self, id: str) -> FHIRPatient:
        result = self.client.get_resource(self.resource_type, id)
        return FHIRPatient.construct(**result)
    
    def create(self, data: Dict[str, Any]) -> FHIRPatient:
        patient = FHIRPatientBuilder.build(data)
        created_resource = self.client.create_resource(patient.dict())
        return FHIRPatient.parse_obj(created_resource)

    def update_patient(self, data: Dict[str, Any]) -> FHIRPatient:
        updated_patient = self.client.update_resource(data)
        return FHIRPatient.parse_obj(updated_patient)
    
    def update_in_bundle(self, data: List[Dict[str, Any]]):
        updated_patients = [FHIRPatientBuilder.build(patient) for patient in data]
        return self.client.update_resources_in_bundle(updated_patients)
    
    def get_patient_by_identifier(self, identifier) -> FHIRPatient:
        params = {
            "identifier": identifier
        }
        results = self.client.search_resources(self.resource_type, params)
        
        if results.get('entry'):
            return FHIRPatient.construct(**results['entry'][0]['resource'])
        return identifier

    @staticmethod
    def filter_data(data) -> Dict[str, Any]:
        filterd_list_data = []
        if isinstance(data, list): 
            for resource_data in data:
                filtered_data = Patient.filter_individual_data(resource_data)
                filterd_list_data.append(filtered_data)
            return filterd_list_data
        filtered_data = Patient.filter_individual_data(data)
        return filtered_data
    
    @staticmethod
    def filter_individual_data(resource_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
                'fhir_id': resource_data.id,
                'given_name': resource_data.name[0].get('given', None),
                'family_name': resource_data.name[0].get('family', None),
                'full_name': resource_data.name[0].get('text', None),
                'birth_date': resource_data.birthDate,
                'gender': resource_data.gender,
                'phone': next((telecom.get('value') for telecom in resource_data.telecom if telecom.get('system') == 'phone'), None),
                'email': next((telecom.get('value') for telecom in resource_data.telecom if telecom.get('system') == 'email'), None),
                'address': Patient._parse_address(resource_data.address[0]) if resource_data.address else None,
                'marital_status': resource_data.maritalStatus.text if resource_data.maritalStatus else None
            }
    @staticmethod
    def _parse_address(data: Dict[str, Any]) -> Dict[str, Any]:
        # Extract latitude and longitude if present
        data["postal_code"] = data.pop("postalCode", None)
        if "extension" in data:
            for ext in data["extension"]:
                if ext.get("url") == "http://hl7.org/fhir/StructureDefinition/geolocation":
                    for geo_ext in ext.get("extension", []):
                        if geo_ext.get("url") == "latitude":
                            data["latitude"] = geo_ext.get("valueDecimal")
                        elif geo_ext.get("url") == "longitude":
                            data["longitude"] = geo_ext.get("valueDecimal")
            
            # Remove the original extension field
            data.pop("extension", None)
        print(data)
        return data

    @staticmethod
    def _parse_name(data: Dict[str, Any]) -> str:
        return " ".join(data.get("given", [])) + " " + data.get("family", "")

    @staticmethod
    def _calculate_age_in_days(birthdate: str) -> int:
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
        today = date.today()
        age = today - birthdate
        return age.days

    @classmethod
    def filter_patient_detail(cls, patient: FHIRPatient) -> Dict[str, Any]:
        return {
            "id": patient.id,
            "name": [cls._parse_name(name.dict()) for name in patient.name],
            "telecom": patient.telecom,
            "gender": patient.gender,
            "birth_date": patient.birthDate,
            "address": [cls._parse_address(address.dict()) for address in patient.address],
            "marital_status": patient.maritalStatus.text if patient.maritalStatus else None,
        }

    @classmethod
    def filter_initial_data(cls, patient: FHIRPatient) -> Dict[str, Any]:
        return {
            "id": patient.id,
            "name": [cls._parse_name(name.dict()) for name in patient.name],
            "age_in_days": cls._calculate_age_in_days(patient.birthDate),
        }

    def get_all_filtered(self) -> List[Dict[str, Any]]:
        patients = self.get_all()
        return [self.filter_initial_data(patient) for patient in patients]

