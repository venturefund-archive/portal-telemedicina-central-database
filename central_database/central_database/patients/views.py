from patients.models import Patient, Vaccine, VaccineStatus
from patients.serializers import (
    PatientSerializer,
    VaccineSerializer,
    VaccineStatusSerializer,
)
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class PatientViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):

    serializer_class = PatientSerializer

    def get_queryset(self):
        queryset = Patient.objects.all()
        return queryset


class VaccineViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):

    serializer_class = VaccineSerializer

    def get_queryset(self):
        queryset = Vaccine.objects.all()
        return queryset


class VaccineStatusViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):

    serializer_class = VaccineStatusSerializer

    def get_queryset(self):
        queryset = VaccineStatus.objects.all()
        return queryset
