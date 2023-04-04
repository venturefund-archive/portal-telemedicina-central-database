from datetime import date

from central_database.integrations.fhir_resources.patient import Patient


def patient_with_twelve_months_in_quarter(client, reference_date_for_quarter=None):
    reference_date = reference_date_for_quarter
    if not reference_date_for_quarter:
        reference_date = date.today()

    quarters = [
        (date(reference_date.year, 1, 1), date(reference_date.year, 4, 30)),
        (date(reference_date.year, 5, 1), date(reference_date.year, 8, 31)),
        (date(reference_date.year, 9, 1), date(reference_date.year, 12, 31)),
    ]

    for i, (start, end) in enumerate(quarters):
        if start <= reference_date <= end:
            current_quarter = quarters[i]

    birth_dates_based_on_quarter = (
        current_quarter[0]
        .replace(year=current_quarter[0].year - 1)
        .strftime("%Y-%m-%d"),
        current_quarter[1]
        .replace(year=current_quarter[1].year - 1)
        .strftime("%Y-%m-%d"),
    )

    query_parameters = {
        "birthdate": [
            f"ge{birth_dates_based_on_quarter[0]}",
            f"le{birth_dates_based_on_quarter[1]}",
        ]
    }

    client = client
    patients_in_current_quarter = Patient(
        id="?", client=client, query_parameters=query_parameters
    )
    list_of_patients = patients_in_current_quarter.all
    list_of_patients_ids = [item["id"] for item in list_of_patients]

    patients_in_current_quarter = list_of_patients_ids

    return patients_in_current_quarter


def number_of_patients_with_completed_doses_in_quarter(
    patients_in_current_quarter, patients_with_completed_doses
):
    patients_in_current_quarter = set(patients_in_current_quarter)
    patients_with_completed_doses = set(patients_with_completed_doses)
    patients_in_current_quarter_with_completed_doses = (
        patients_in_current_quarter & patients_with_completed_doses
    )

    numerator = len(patients_in_current_quarter_with_completed_doses)
    return numerator


def calculate_denominator(client):
    identified_denominator = client.children_registered_in_APS
    estimated_denominator = (
        client.sisab_municipal_registration / client.ibge_population
    ) * client.children_born_alive

    denominator = estimated_denominator
    if identified_denominator >= (0.85 * estimated_denominator):
        denominator = identified_denominator

    return denominator


def calculate_immunization_indicator(client, patients_with_completed_doses):
    patients_in_current_quarter = patient_with_twelve_months_in_quarter(client)

    numerator = number_of_patients_with_completed_doses_in_quarter(
        patients_in_current_quarter, patients_with_completed_doses
    )
    denominator = calculate_denominator(client)

    return numerator / denominator
