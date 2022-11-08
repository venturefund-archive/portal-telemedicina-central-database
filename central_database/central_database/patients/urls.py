from django.urls import path

from central_database.patients.views import (  # noqa: E501
    PatientDetailView,
    PatientImmunizationView,
)

app_name = "patients"
urlpatterns = [
    path("<int:id>/", PatientDetailView.as_view()),
    path("<int:id>/immunization/", PatientImmunizationView.as_view()),  # noqa: E501
]
