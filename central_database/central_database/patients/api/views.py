from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

import central_database.integrations.fhir_resources.patient as patient_resource
from central_database.customers.models import Client


class PatientsViewSet(ViewSet):
    def list(self, request):
        client_id = request.user.client_id
        client = Client.objects.get(id=client_id)
        patients = patient_resource.Patient(client=client)
        data = patients.all
        return Response(data)

    def retrieve(self, request, pk=None):
        client_id = request.user.client_id
        client = Client.objects.get(id=client_id)
        patient = patient_resource.Patient(id=pk, client=client)
        data = patient.detail
        return Response(data)
