from rest_framework import serializers

from central_database.permissions_manager.rest_api.mixins import (
    PermissionSerializerMixin,
)
from central_database.vaccines.models import Vaccine, VaccineAlert, VaccineDose


class VaccineSerializer(
    PermissionSerializerMixin, serializers.ModelSerializer
):  # noqa: E501
    class Meta:
        model = Vaccine
        fields = "__all__"


class VaccineAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineAlert
        fields = "__all__"


class VaccineDosesSerializer(
    PermissionSerializerMixin, serializers.ModelSerializer
):  # noqa: E501
    alerts = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField(method_name="get_status")

    class Meta:
        model = VaccineDose
        fields = [
            "id",
            "vaccine",
            "minimum_recommended_age",
            "maximum_recommended_age",
            "dose_order",
            "gender_recommendation",
            "alerts",
            "is_completed",
        ]

    def get_alerts(self, vaccine_dose_instance):
        patient_id = self.context.get("patient_id")
        alerts = vaccine_dose_instance.get_vaccine_alerts(
            patient_id=patient_id
        )  # noqa: E501
        return VaccineAlertSerializer(alerts, many=True).data

    def get_status(self, vaccine_dose_instance):
        patient_id = self.context.get("patient_id")
        status = vaccine_dose_instance.get_vaccine_status(
            patient_id=patient_id
        ).first()  # noqa: E501
        if status:
            return status.completed
        return None
