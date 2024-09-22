from django.core.management.base import BaseCommand
from integrations.fhir.fhir_resources.patient import Patient
from customers.models import Client
from typing import Dict, Any, List
import csv
import pandas as pd
from datetime import datetime

class Command(BaseCommand):
    help = 'Parse external data and create patients'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('client_name', type=str, help='Client name')

    def handle(self, *args, **options):
        client_name = options["client_name"]
        csv_file_path = options['csv_file']
        token = "eyJraWQiOiJybmRzIGF1dGgiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIwNjU1MzU2NDAwMDEzOCIsInBlc3NvYSI6eyJmaXNpY2EiOmZhbHNlLCJpZGVudGlmaWNhZG9yIjoiMDY1NTM1NjQwMDAxMzgifSwiaXNzIjoiUk5EUyIsImV4cCI6MTcyNjg3NjU1NiwiaWF0IjoxNzI2ODc0NzU2LCJjZXJ0aWZpY2FkbyI6eyJzdWJqZWN0IjoiQ049UElBVUkgU0VDUkVUQVJJQSBERSBTQVVERTowNjU1MzU2NDAwMDEzOCxPVT1SRkIgZS1DTlBKIEExLE9VPUFSQVRJUEksT1U9U2VjcmV0YXJpYSBkYSBSZWNlaXRhIEZlZGVyYWwgZG8gQnJhc2lsIC0gUkZCLE9VPTA4ODM5MTM1MDAwMTU3LE9VPXByZXNlbmNpYWwsTz1JQ1AtQnJhc2lsLEw9VEVSRVNJTkUsU1Q9UEksQz1CUiIsImlzc3VlciI6IkNOPUF1dG9yaWRhZGUgQ2VydGlmaWNhZG9yYSBTRVJQUk9SRkJ2NSwgT1U9U2VjcmV0YXJpYSBkYSBSZWNlaXRhIEZlZGVyYWwgZG8gQnJhc2lsIC0gUkZCLCBPPUlDUC1CcmFzaWwsIEM9QlIiLCJzZXJpYWxOdW1iZXIiOiIwMDowMDowMDowMDowMDowMDpFMzo1NzpBQzo3MTozOToyNjo0OTo3NDo2QTpFOTpGMDoyMSIsIm1kNSI6IkY0OjY0OkM2OjNFOkM5OjZGOjYwOkIzOkRBOkU0Ojg0OjYzOjQ2OjdEOjhBOkRBIiwic2hhMSI6IjIyOjUzOkFCOkZCOjYwOjRFOjhGOkY5OkVEOkU2OkEzOjU5OjBFOjlDOjE5OjdEOjY2OjVCOjNEOjk5Iiwic2hhMjU2IjoiMDA6Nzg6MEQ6QTc6OEQ6NkE6Nzg6NkM6NjY6NTQ6OTE6N0M6MTA6Nzc6RDQ6M0E6MEM6NUE6QTU6MkU6NTI6RDI6NEU6M0E6MzA6RDU6MEE6QzA6MzM6Nzk6ODQ6MjUiLCJrZXlNb2R1bHVzIjoiMjUyOTk2NjIwMzc0NTE5ODE0NTAwODk3OTc4OTEyNDEzNTQyMTI0NzAzODI5MTA2NzU0MzQ0NTM2MjYyNzg4ODc5NTEwMTAwNzg3ODI3NjM3OTMyMjcxNzk2NDgwODUzODAwMDgzNDA4MTkxNzc4NDM3NDQwNTQyNDczMjY5ODU0NDE3MDkzMjYxOTA2NTM5NTY0OTM3NzgzOTQ4ODI1NDY3MzY4NjIzOTk5OTQxMDk1MzMxNjIyOTc5ODQ2NTQ2MjkwMTI4NDI5OTMyMjE5NDI4ODE5NzA1MjYyMjg0NTAzODg3OTM0ODk0ODExODY4NTIxMzI0Njg2MDk2NzA2OTg3MjY3MDgyMTAyNTI4NDk1MzExMDE4ODU3OTAxOTIzODM2NDE3MzE3MjAzMzA5MzU0MTUyNzgwNzEzODI5NzMyMDk1MzU5MDc3NjA5NTMyNTE4MjI5OTMwNzc0NzI4MDY2MjMyNzgyNjM1NDk2NjY5ODQ4ODk2NzYxMjQ5MjA3NzQxNjYxMTkxMTM0ODcxMzQ4NjkzMTkzMzI2NDY2NzY5NTc3OTYwNTE5NDkyNjcwMTE3MDE2NjE0MjIyMzY4Mzg1MTI5MjczMTcyMDM3MjIzMTM0NTc1NzgwOTI2MDU2MDYwMDA2NTg3MjU1NjY1Nzk3NTc5MTg0NTg2OTk5MTM4MjE2MjQzNTYyMzU2MDYzODE0NTgxNTEwMDg5ODM2MzgxOTIxOTcwMzkwNDk0MTc4ODQ3MDMzNzE2NjQxMTkzNjUzMTA2MTgzMTM0NjMxMzg0MzM0MDA1NTAwOTAwNjY0NDk2ODE3MjkiLCJrZXlFeHBvbmVudCI6IjY1NTM3IiwiaXNzdWVyU2VyaWFsTnVtYmVyIjoiMDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MDA6MEIiLCJpc3N1ZXJTaGEyNTZGaW5nZXJwcmludCI6IkIxOkU5OjNBOjAyOjU0OjExOkZFOkQ2OjIzOjE2OkU5Ojk5OjUzOkQ2OjE0OjQ2OkYxOkJDOjNDOjIwOjVGOjdEOjhBOjc0OjZDOjREOjgxOjQ5OkMyOjQ5OjU5OkFCIn19.MKWs8cmeoUkaT_v5AJy2CYqgacp_QIHCzhi2ESDYE1xzG4T_gJ2UsfhHlK-eQgGiWNgWO6XMIHueWs-a4w6FWKeQv39Pwfak5p_okIC4vn5vZeJ8qlOdgwHJoFXqH1-r9mHnKNThHyWctz6BqvgkT8ZOZWx_jS5F8mp_6cGcY4AxjfxfGvRq5k-KygZ014kYY6UsHq9AHz8zQhDZn_gP_3GKI1ezlDavxZ2emD8FMR_CauKmPjahnVCsscXBGkXWOiA4jdHBHG5hqA4ItzlNXDn4HG3OICohoFnftMjNIiwfCNLNMDRTYWACNHi89enLA80GWkSunAPNY9aOqu-J8Q"
        client = Client.objects.get(client_name=client_name)

        patient_service = Patient(client=client, client_type='google')

        csv_patients = self.read_csv_patients(csv_file_path)
        fhir_patients = patient_service.get_all_pages_resources()

        fhir_df = self.create_fhir_dataframe(fhir_patients)
        csv_df = self.create_csv_dataframe(csv_patients)

        # Compare the dataframes
        self.compare_dataframes(fhir_df, csv_df)

    def read_csv_patients(self, csv_file_path: str) -> List[Dict[str, str]]:
        patients = []
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                patients.append(row)
        return patients

    def create_fhir_dataframe(self, fhir_patients: List[Dict[str, Any]]) -> pd.DataFrame:
        data = []
        for patient in fhir_patients:
            if patient.identifier:
                for identifier in patient.identifier:
                    if identifier.get('system') == 'http://rnds.saude.gov.br/fhir/r4/NamingSystem/cns':
                        cns = identifier.get('value')
                    elif identifier.get('system') == 'http://rnds.saude.gov.br/fhir/r4/NamingSystem/cpf':
                        cpf = identifier.get('value')
            else:
                cns = None
                cpf = None
            birthdate = patient.birthDate
            data.append({'cns': cns, 'cpf': cpf, 'birthdate': birthdate})
        return pd.DataFrame(data)

    def create_csv_dataframe(self, csv_patients: List[Dict[str, str]]) -> pd.DataFrame:
        data = []
        for patient in csv_patients:
            cns = patient.get('identifier_cns')
            cpf = patient.get('identifier_cpf')
            birthdate = patient.get('birthdate')
            # Convert birthdate to YYYY-MM-DD format if necessary
            if birthdate:
                try:
                    birthdate = datetime.strptime(birthdate, '%d/%m/%Y').strftime('%Y-%m-%d')
                except ValueError:
                    pass  # Keep original format if conversion fails
            data.append({'cns': cns, 'cpf': cpf, 'birthdate': birthdate})
        return pd.DataFrame(data)

    def compare_dataframes(self, fhir_df: pd.DataFrame, csv_df: pd.DataFrame):
        print(f"FHIR patients: {len(fhir_df)}")
        print(f"CSV patients: {len(csv_df)}")

        extra_ids = self.create_csv_dataframe(self.read_csv_patients("extra_ids.csv"))
        extra_ids = set(extra_ids['cns'])

        # Create sets for efficient lookup
        csv_cns_set = set(csv_df['cns'].dropna())
        csv_cpf_set = set(csv_df['cpf'].dropna())

        matched = 0
        not_found = 0

        list_of_unmatched = []
        for _, fhir_patient in fhir_df.iterrows():
            fhir_cns = fhir_patient['cns']

            if pd.notna(fhir_cns) and fhir_cns in csv_cns_set:
                matched += 1
            else:
                list_of_unmatched.append({
                    'cns': fhir_cns if pd.notna(fhir_cns) else '',
                })
                not_found += 1

        print(f"Matched patients: {matched}")
        print(f"Unmatched patients: {not_found}")

        with open('unmatched_patients_fhir.csv', 'w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=['cns', 'cpf', 'birthdate'])
            csv_writer.writeheader()
            for patient in list_of_unmatched:
                csv_writer.writerow(patient)
