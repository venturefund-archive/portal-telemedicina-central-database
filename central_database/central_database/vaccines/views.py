from django.shortcuts import render  # noqa: F401
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from central_database.vaccines.models import VaccineDose
from central_database.vaccines.serializers import VaccineDosesSerializer


class VaccineDosesViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):

    serializer_class = VaccineDosesSerializer

    def get_queryset(self):
        return VaccineDose.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        parameter = self.request.query_params.get("patient_id")
        if parameter:
            context.update({"patient_id": parameter})
        return context
