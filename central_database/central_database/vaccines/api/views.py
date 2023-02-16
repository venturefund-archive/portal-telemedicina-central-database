from django.shortcuts import render  # noqa: F401
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from central_database.permissions_manager.rest_api.permission_classes import (
    permission_class_assembler,
)
from central_database.vaccines.api.serializers import (
    VaccineDosesSerializer,
    VaccineProtocolSerializer,
    VaccineSerializer,
)
from central_database.vaccines.models import (  # noqa: E501
    Vaccine,
    VaccineDose,
    VaccineProtocol,
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

    def get_queryset(self):
        return VaccineDose.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        parameter = self.request.query_params.get("patient_id")
        if parameter:
            context.update({"patient_id": parameter})
        return context


class VaccineViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):

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
