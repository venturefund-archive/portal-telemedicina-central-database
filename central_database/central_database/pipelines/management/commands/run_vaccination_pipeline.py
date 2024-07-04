from datetime import datetime

import pandas as pd
from django.core.management.base import BaseCommand
from google.cloud import bigquery

from central_database.customers.models import Client
from central_database.vaccines.models import (  # noqa: E501
    VaccineAlert,
    VaccineDose,
    VaccineStatus,
)


class Command(BaseCommand):
    help = "Runs the vaccination pipeline"

    def get_vaccination_source(self, path_to_csv):
        df = pd.read_csv(path_to_csv)
        return df

    def get_data_from_bigquery(self, query):
        client = bigquery.Client()
        query_job = client.query(query)
        results = query_job.result()
        df = results.to_dataframe()
        return df

    def run_vaccination_pipeline(self):
        city = "taruma"
        client = Client.get_client_by_city(city)
        if not client:
            return print(f"No client for city: {city} found")

        fhir_store = client.fhir_store

        query = """
            SELECT * FROM
            `ptm-gestao-di-dev.immunization_data.taruma_vaccination_data_cleaned`
        """
        vaccination_report = self.get_data_from_bigquery(query)
        vaccination_report = vaccination_report.drop_duplicates(
            subset=["fhir_id", "dose_id"], keep="first"
        )

        vaccination_report_grouped_by_fhir_id = vaccination_report.groupby(
            "fhir_id"
        )  # noqa: E501

        for name, group in vaccination_report_grouped_by_fhir_id:
            vaccine_status = VaccineStatus.insert_vaccine_status_in_bulk(
                group, fhir_store
            )
            print(
                f"{len(vaccine_status)} completed doses created for patient {name}"  # noqa: E501
            )

            vaccine_status_id = set(
                VaccineStatus.objects.filter(patient_id=name).values_list(
                    "vaccine_dose_id", flat=True
                )
            )
            vaccine_doses_objects = VaccineDose.objects.all()
            vaccine_doses_id = set(
                vaccine_doses_objects.values_list("id", flat=True)
            )  # noqa: E501
            vaccine_not_completed = list(vaccine_doses_id - vaccine_status_id)
            vaccine_alerts_id = []

            today = datetime.today().date()
            birthdate = group.birthdate.unique()[0]
            age_in_months = int(((today - birthdate).days / 365) * 12)

            for vaccine_dose in vaccine_doses_objects.filter(
                id__in=vaccine_not_completed
            ):
                if age_in_months > vaccine_dose.maximum_recommended_age:
                    vaccine_alerts_id.append(vaccine_dose.id)

            vaccine_alerts = VaccineAlert.insert_vaccine_alerts_in_bulk(
                name, vaccine_alerts_id, fhir_store
            )
            print(
                f"{len(vaccine_alerts)} alerts doses created for patient {name}"  # noqa: E501
            )

    def handle(self, *args, **options):
        self.run_vaccination_pipeline()
