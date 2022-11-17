from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

import central_database.integrations.fhir_resources.patient as patient_resource


class PatientsViewSet(ViewSet):
    def list(self, request):
        patients = patient_resource.Patient()
        data = patients.all
        return Response(data)

    def retrieve(self, request, pk=None):
        patient = patient_resource.Patient(id=pk)
        data = patient.detail
        return Response(data)
