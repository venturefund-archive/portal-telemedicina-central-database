from datetime import date, datetime


def calculate_age_in_days(birthdate):
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
    today = date.today()

    age = today - birthdate
    return age.days
