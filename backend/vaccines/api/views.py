from django.db.models import Prefetch
from django.shortcuts import render  # noqa: F401
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from integrations.fhir.views import FHIRBaseViewSet
from rest_framework.mixins import (  # noqa: E501
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status


from integrations.fhir.fhir_resources.immunization import Immunization as FHIRImmunization
from integrations.fhir.fhir_resources.immunization_recommendation import ImmunizationRecommendation as FHIRImmunizationRecommendation

from permissions_manager.rest_api.permission_classes import (
    permission_class_assembler,
)
from vaccines.api.filters import (  # noqa: E501
    VaccineDoseFilterSet,
    VaccineFilterSet,
    ImmunizationRecommendationFilterSet,
    ImmunizationFilterSet
)
from vaccines.api.serializers import (
    VaccinationCardSerializer,
    VaccineDosesSerializer,
    VaccineSerializer,
    ImmunizationRecommendationSerializer,
    ImmunizationSerializer,
    VaccineProtocolSerializer
)
from vaccines.models import (  # noqa: E501
    VaccinationCard,
    Vaccine,
    VaccineDose,
    VaccineProtocol,
    Immunization,
    ImmunizationRecommendation
)


class ImmunizationRecommendationViewSet(FHIRBaseViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = ImmunizationRecommendationSerializer
    filterset_class = ImmunizationRecommendationFilterSet

    permission_classes = [
        IsAuthenticated,
        permission_class_assembler(
            permissions_to_check={
                "list": ["vaccines.view_immunizationrecommendation"],
                "create": ["vaccines.add_immunizationrecommendation"],
            }
        ),
    ]
    fhir_resource_class = FHIRImmunizationRecommendation

    def list(self, request, *args, **kwargs):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return JsonResponse({"error": "Patient ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        fhir_data = self._handle_fhir_operation('get_patient_immunization_recommendations', patient_id)
        if fhir_data is not None:
            serializer = self.get_serializer(data=fhir_data, many=True)
            serializer.is_valid(raise_exception=True)
            return JsonResponse(serializer.data, safe=False)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        fhir_data = self._handle_fhir_operation('create', serializer.validated_data)
        if fhir_data is not None:
            return Response(fhir_data, status=status.HTTP_201_CREATED)
        else:
            recommendation = serializer.save()
            return Response(self.get_serializer(recommendation).data, status=status.HTTP_201_CREATED)
        
    @action(detail=True, methods=['post'])
    def silence_alert(self, request, pk=None):
        recommendation = self.get_object()
        recommendation.silence_alert(request.user)
        
        if self.fhir_resource_class:
            fhir_data = self._handle_fhir_operation('update', recommendation)
            if fhir_data is not None:
                return Response(fhir_data)
        
        serializer = self.get_serializer(recommendation)
        return Response(serializer.data)


class ImmunizationViewSet(FHIRBaseViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = ImmunizationSerializer
    filterset_class = ImmunizationFilterSet

    permission_classes = [
        IsAuthenticated,
        permission_class_assembler(
            permissions_to_check={
                "list": ["vaccines.view_immunization"],
                "create": ["vaccines.add_immunization"],
            }
        ),
    ]
    fhir_resource_class = FHIRImmunization


    def list(self, request, *args, **kwargs):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return JsonResponse({"error": "Patient ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        fhir_data = self._handle_fhir_operation('get_patient_immunizations', patient_id)
        if fhir_data is not None:
            serializer = self.get_serializer(data=fhir_data, many=True)
            serializer.is_valid(raise_exception=True)
            return JsonResponse(serializer.data, safe=False)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        fhir_data = self._handle_fhir_operation('create', serializer.validated_data)
        if fhir_data is not None:
            return JsonResponse(fhir_data, status=status.HTTP_201_CREATED)
        else:
            immunization = serializer.save()
            return JsonResponse(self.get_serializer(immunization).data, status=status.HTTP_201_CREATED)


class VaccineDosesViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):

    filter_backends = [DjangoFilterBackend]
    filterset_class = VaccineDoseFilterSet
    serializer_class = VaccineDosesSerializer
    permission_classes = [
        IsAuthenticated,
        permission_class_assembler(
            permissions_to_check={
                "list": ["vaccines.view_vaccinedose"],
                "retrieve": ["vaccines.view_vaccinedose"],
            }
        ),
    ]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="patient_id",
                description="ID of the patient",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY,
            )
        ],
        responses={200: VaccineDosesSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        patient_id = self.request.query_params.get("patient_id")
        return VaccineDose.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        parameter = self.request.query_params.get("patient_id")
        if parameter:
            context.update({"patient_id": parameter})
        return context


class VaccineViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):

    filter_backends = [DjangoFilterBackend]
    filterset_class = VaccineFilterSet
    serializer_class = VaccineSerializer
    permission_classes = [
        IsAuthenticated,
        permission_class_assembler(
            permissions_to_check={
                "list": ["vaccines.view_vaccine"],
                "retrieve": ["vaccines.view_vaccine"],
            }
        ),
    ]

    def get_queryset(self):
        return Vaccine.objects.all()


class VaccineProtocolMetricsViewSet(GenericViewSet, RetrieveModelMixin):
    serializer_class = VaccineProtocolSerializer

    def get_queryset(self):
        return VaccineProtocol.objects.all()


class VaccinationCardViewSet(GenericViewSet, CreateModelMixin):

    serializer_class = VaccinationCardSerializer

    def get_queryset(self):
        return VaccinationCard.objects.all()