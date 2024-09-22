import json
from rest_framework import status
from rest_framework.mixins import (  # noqa: E501
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from integrations.fhir.fhir_resources.patient import Patient as FHIRPatient
from integrations.fhir.views import FHIRBaseViewSet
from permissions_manager.rest_api.permission_classes import (
    permission_class_assembler,
)
from services.cache_service import CacheService
from patients.api.serializers import PatientMapSerializer, PatientSerializer


class PatientsViewSet(
    FHIRBaseViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
):
    serializer_class = PatientSerializer
    permission_classes = [
        IsAuthenticated,
        permission_class_assembler(
            permissions_to_check={
                "list": ["patients.view_patient"],
                "retrieve": ["patients.view_patient"],
                "update": ["patients.change_patient"],
                "partial_update": ["patients.change_patient"],
            }
        ),
    ]

    fhir_resource_class = FHIRPatient

    def list(self, request, *args, **kwargs):
        fhir_data = self._handle_fhir_operation('get_all_pages_resources')
        if fhir_data is not None:
            serializer = self.get_serializer(data=fhir_data, many=True)
            serializer.is_valid(raise_exception=True)
            return JsonResponse(serializer.data, safe=False)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(detail=False, methods=['GET'])
    def search(self, request):
        query = request.query_params.get('q', '').lower()
        if query:
            patient_ids = self.redis.smembers(f"patient_search:{query}")
            patients = []
            for patient_id in patient_ids:
                patient_data = self.redis.get(f"patient:{patient_id.decode()}")
                if patient_data:
                    patients.append(json.loads(patient_data))
            serializer = self.get_serializer(data=patients, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)
        return Response([])

    def retrieve(self, request, *args, **kwargs):
        fhir_data = self._handle_fhir_operation('get_patient_by_id', kwargs['pk'])
        if fhir_data is not None:
            return Response(fhir_data)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        updated_patient = instance.update(request.data)
        return Response(updated_patient)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def map_data(self, request):
        patients = self.get_queryset()
        serializer = PatientMapSerializer(patients, many=True)
        return Response(serializer.data)