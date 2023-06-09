from django.db.models import Prefetch
from django.shortcuts import render  # noqa: F401
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework.decorators import action
from rest_framework.mixins import (  # noqa: E501
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from central_database.permissions_manager.rest_api.permission_classes import (
    permission_class_assembler,
)
from central_database.vaccines.api.filters import VaccineFilterSet
from central_database.vaccines.api.serializers import (
    VaccineAlertSerializer,
    VaccineDosesSerializer,
    VaccineProtocolSerializer,
    VaccineSerializer,
)
from central_database.vaccines.models import (  # noqa: E501
    Vaccine,
    VaccineAlert,
    VaccineDose,
    VaccineProtocol,
    VaccineStatus,
)


class VaccineDosesViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):

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
        return VaccineDose.objects.all().prefetch_related(
            Prefetch(
                "vaccine_alerts",
                queryset=VaccineAlert.objects.filter(patient_id=patient_id),
                to_attr="active_alerts",
            ),
            Prefetch(
                "vaccinestatus_set",
                queryset=VaccineStatus.objects.filter(patient_id=patient_id),
                to_attr="patient_status",
            ),
        )

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


class VaccineAlertViewSet(GenericViewSet, UpdateModelMixin):
    serializer_class = VaccineAlertSerializer

    def get_queryset(self):
        return VaccineAlert.objects.all()

    @action(detail=True, methods=["patch"], url_path="deactivate")
    def deactivate_alert(self, request, pk=None):
        alert = self.get_object()
        alert.active = False
        alert.save()
        serializer = self.get_serializer(alert)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="activate")
    def activate_alert(self, request, pk=None):
        alert = self.get_object()
        alert.active = True
        alert.save()
        serializer = self.get_serializer(alert)
        return Response(serializer.data)
