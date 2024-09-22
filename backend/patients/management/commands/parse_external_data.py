import csv
import requests
from typing import Dict, Any
from django.core.management.base import BaseCommand
from integrations.fhir.fhir_resources.patient import Patient
from customers.models import Client

class Command(BaseCommand):
    help = 'Process CSV and create FHIR patients'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='Path to the CSV file containing patient data')
        parser.add_argument('client_name', type=str, help='Client name')

    def handle(self, *args, **options):
        client_name = options["client_name"]
        csv_file_path = options['csv_file_path']
        token = "eyJraWQiOiJybmRzIGF1dGgiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIwNjU1MzU2NDAwMDEzOCIsInBlc3NvYSI6eyJmaXNpY2EiOmZhbHNlLCJpZGVudGlmaWNhZG9yIjoiMDY1NTM1NjQwMDAxMzgifSwiaXNzIjoiUk5EUyIsImV4cCI6MTcyNjk0NTc0NSwiaWF0IjoxNzI2OTQzOTQ1LCJjZXJ0aWZpY2FkbyI6eyJzdWJqZWN0IjoiQ049UElBVUkgU0VDUkVUQVJJQSBERSBTQVVERTowNjU1MzU2NDAwMDEzOCxPVT1SRkIgZS1DTlBKIEExLE9VPUFSQVRJUEksT1U9U2VjcmV0YXJpYSBkYSBSZWNlaXRhIEZlZGVyYWwgZG8gQnJhc2lsIC0gUkZCLE9VPTA4ODM5MTM1MDAwMTU3LE9VPXByZXNlbmNpYWwsTz1JQ1AtQnJhc2lsLEw9VEVSRVNJTkEsU1Q9UEksQz1CUiIsImlzc3VlciI6IkNOPUF1dG9yaWRhZGUgQ2VydGlmaWNhZG9yYSBTRVJQUk9SRkJ2NSwgT1U9U2VjcmV0YXJpYSBkYSBSZWNlaXRhIEZlZGVyYWwgZG8gQnJhc2lsIC0gUkZCLCBPPUlDUC1CcmFzaWwsIEM9QlIiLCJzZXJpYWxOdW1iZXIiOiIwMDowMDowMDowMDowMDowMDpFMzo1NzpBQzo3MTozOToyNjo0OTo3NDo2QTpFOTpGMDoyMSIsIm1kNSI6IkY0OjY0OkM2OjNFOkM5OjZGOjYwOkIzOkRBOkU0Ojg0OjYzOjQ2OjdEOjhBOkRBIiwic2hhMSI6IjIyOjUzOkFCOkZCOjYwOjRFOjhGOkY5OkVEOkU2OkEzOjU5OjBFOjlDOjE5OjdEOjY2OjVCOjNEOjk5Iiwic2hhMjU2IjoiMDA6Nzg6MEQ6QTc6OEQ6NkE6Nzg6NkM6NjY6NTQ6OTE6N0M6MTA6Nzc6RDQ6M0E6MEM6NUE6QTU6MkU6NTI6RDI6NEU6M0E6MzA6RDU6MEE6QzA6MzM6Nzk6ODQ6MjUiLCJrZXlNb2R1bHVzIjoiMjUyOTk2NjIwMzc0NTE5ODE0NTAwODk3OTc4OTEyNDEzNTQyMTI0NzAzODI5MTA2NzU0MzQ0NTM2MjYyNzg4ODc5NTEwMTAwNzg3ODI3NjM3OTMyMjcxNzk2NDgwODUzODAwMDgzNDA4MTkxNzc4NDM3NDQwNTQyNDczMjY5ODU0NDE3MDkzMjYxOTA2NTM5NTY0OTM3NzgzOTQ4ODI1NDY3MzY4NjIzOTk5OTQxMDk1MzMxNjIyOTc5ODQ2NTQ2MjkwMTI4NDI5OTMyMjE5NDI4ODE5NzA1MjYyMjg0NTAzODg3OTM0ODk0ODExODY4NTIxMzI0Njg2MDk2NzA2OTg3MjY3MDgyMTAyNTI4NDk1MzExMDE4ODU3OTAxOTIzODM2NDE3MzE3MjAzMzA5MzU0MTUyNzgwNzEzODI5NzMyMDk1MzU5MDc3NjA5NTMyNTE4MjI5OTMwNzc0NzI4MDY2MjMyNzgyNjM1NDk2NjY5ODQ4ODk2NzYxMjQ5MjA3NzQxNjYxMTkxMTM0ODcxMzQ4NjkzMTkzMzI2NDY2NzY5NTc3OTYwNTE5NDkyNjcwMTE3MDE2NjE0MjIyMzY4Mzg1MTI5MjczMTcyMDM3MjIzMTM0NTc1NzgwOTI2MDU2MDYwMDA2NTg3MjU1NjY1Nzk3NTc5MTg0NTg2OTk5MTM4MjE2MjQzNTYyMzU2MDYzODE0NTgxNTEwMDg5ODM2MzgxOTIxOTcwMzkwNDk0MTc4ODQ3MDMzNzE2NjQxMTkzNjUzMTA2MTgzMTM0NjMxMzg0MzM0MDA1NTAwOTAwNjY0NDk2ODE3MjkiLCJrZXlFeHBvbmVudCI6IjY1NTM3IiwiaXNzdWVyU2VyaWFsTnVtYmVyIjoiMDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MEIiLCJpc3N1ZXJTaGEyNTZGaW5nZXJwcmludCI6IkIxOkU5OjNBOjAyOjU0OjExOkZFOkQ2OjIzOjE2OkU5Ojk5OjUzOkQ2OjE0OjQ2OkYxOkJDOjNDOjIwOjVGOjdEOjhBOjc0OjZDOjREOjgxOjQ5OkMyOjQ5OjU5OkFCIn19.Q8VhEtR6iJxvZ5LRzNER_J8k3FLgl7Dm_bU23YAnxteJs13rgn-VWBrZxOCO_ZygUFt5PmTZcCMrAYJtpGBz0gjowEK_QuGDlcndhAEn6p2Mw9hptx5rpoD7Jr1pJ98jgxGgn4GBay9wg6oiEyIdpYtWThy_pQV7EYChigKpIHSwHoRyIK1tMUW43YGPGLeT57nqiRdAzaBzzz332htZH4uuiXVW_lDRGo5Dn22rLOJdxFImpugwraCzBPDXX9tqhpASPfgQmCU5cJW97FFAS6mxz_WnxiE2vsPTCczKPtdAo6yFcqprWArB4pwI_pFbgc4cMWdrFQHCtRw74cJQBg"
        client = Client.objects.get(client_name=client_name)

        patient_service = Patient(client=client, client_type='google')

        self.process_csv_and_create_patients(csv_file_path, token, patient_service)

    def process_csv_and_create_patients(self, csv_file_path: str, token: str, patient_service: Patient):
        count = 0
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                patient_data = self.fetch_patient_data(row, token)
                if patient_data:
                    # fhir_patient = patient_service.create(patient_data)
                    print(f'Created patient: {patient_data}')
                    count += 1
                    print(f'Count: {count}')
    def fetch_patient_data(self, row: Dict[str, str], token: str) -> Dict[str, Any]:
        base_url = "https://pi-ehr-services.saude.gov.br/api/fhir/r4/Patient"
        headers = {
            "Content-Type": "application/json",
            "X-Authorization-Server": f"Bearer {token}",
            "Authorization": "700408903945949"
        }

        if row['identifier_cpf']:
            identifier = f"http://rnds.saude.gov.br/fhir/r4/NamingSystem/cpf|{row['identifier_cpf']}"
        elif row['identifier_cns']:
            identifier = f"http://rnds.saude.gov.br/fhir/r4/NamingSystem/cns|{row['identifier_cns']}"
        else:
            print(f"No valid identifier found for row: {row}")
            return None
        print(f"Identifier: {identifier}")
        params = {"identifier": identifier}
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            fhir_data = response.json()
            if fhir_data['total'] > 0:
                patient_resource = fhir_data['entry'][0]['resource']
                return self.extract_patient_data(patient_resource)
        else:
            print(f"Error fetching data for identifier {identifier}: {response.status_code}")
        return None

    def extract_patient_data(self, patient_resource: Dict[str, Any]) -> Dict[str, Any]:
        data = {
            'id': patient_resource.get('id'),
            'name': patient_resource['name'][0]['text'] if patient_resource.get('name') else None,
            'gender': patient_resource.get('gender'),
            'birth_date': patient_resource.get('birthDate'),
            'telecom': next((t['value'] for t in patient_resource.get('telecom', []) if t['system'] == 'phone'), None),
            'address': {
                'line': patient_resource['address'][0].get('line', []) if patient_resource.get('address') else [],
                'city': patient_resource['address'][0].get('city') if patient_resource.get('address') else None,
                'district': patient_resource['address'][0].get('district') if patient_resource.get('address') else None,
                'state': patient_resource['address'][0].get('state') if patient_resource.get('address') else None,
                'postal_code': patient_resource['address'][0].get('postalCode') if patient_resource.get('address') else None,
                'country': patient_resource['address'][0].get('country') if patient_resource.get('address') else None,
            }
        }

        identifiers = []
        for identifier in patient_resource.get('identifier', []):
            identifiers.append({
                'system': identifier['system'],
                'value': identifier['value'],
                'use': identifier.get('use', 'official')
            })
        data["identifier"] = identifiers

        return data
        