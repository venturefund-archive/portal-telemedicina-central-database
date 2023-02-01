from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

import central_database.integrations.fhir_resources.patient as patient_resource
from central_database.customers.models import Client
from central_database.permissions_manager.rest_api.permission_classes import (
    permission_class_assembler,
)


class PatientsViewSet(ViewSet):

    permission_classes = [
        IsAuthenticated,
        permission_class_assembler(
            permissions_to_check={
                "list": ["patients.can_view_patient"],
                "retrieve": ["patients.can_view_patient"],
            }
        ),
    ]

    def list(self, request):
        client_id = request.user.client_id
        client = Client.objects.filter(id=client_id)
        patients = patient_resource.Patient(id="?", client=client.first())
        data = patients.all
        return Response(data)

    def retrieve(self, request, pk=None):
        client_id = request.user.client_id
        client = Client.objects.filter(id=client_id)
        patient = patient_resource.Patient(id=pk, client=client.first())
        data = patient.detail
        return Response(data)
