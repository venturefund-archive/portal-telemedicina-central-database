from rest_framework import serializers

from central_database.permissions_manager.rest_api.mixins import (
    PermissionSerializerMixin,
)
from central_database.vaccines.models import (
    Vaccine,
    VaccineAlert,
    VaccineDose,
    VaccineProtocol,
    VaccineStatus,
)


class VaccineSerializer(serializers.ModelSerializer
):  # noqa: E501
    class Meta:
        model = Vaccine
        fields = "__all__"


class VaccineAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineAlert
        fields = "__all__"


class VaccineDosesSerializer(
    serializers.ModelSerializer
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
        alerts = vaccine_dose_instance.active_alerts
        return VaccineAlertSerializer(alerts, many=True).data

    def get_status(self, vaccine_dose_instance):
        status = vaccine_dose_instance.patient_status[0] if vaccine_dose_instance.patient_status else None
        if status:
            return status.completed
        return None


class VaccineProtocolSerializer(
    PermissionSerializerMixin, serializers.ModelSerializer
):  # noqa: E501
    vaccine_doses = VaccineDosesSerializer(many=True)
    completed_doses_count = serializers.SerializerMethodField()
    completed_doses_percentage = serializers.SerializerMethodField()
    alert_doses_count = serializers.SerializerMethodField()
    expected_doses_count = serializers.SerializerMethodField()

    class Meta:
        model = VaccineProtocol
        fields = [
            "id",
            "vaccine_doses",
            "completed_doses_count",
            "completed_doses_percentage",
            "alert_doses_count",
            "expected_doses_count",
        ]

    def get_completed_doses_count(self, vaccine_protocol_instance):
        return vaccine_protocol_instance.get_total_amount_of_completed_doses()

    def get_alert_doses_count(self, vaccine_protocol_instance):
        return vaccine_protocol_instance.get_total_amount_of_alert_doses()

    def get_expected_doses_count(self, vaccine_protocol_instance):
        completed_doses_count = self.get_completed_doses_count(
            vaccine_protocol_instance
        )
        alert_doses_count = self.get_alert_doses_count(
            vaccine_protocol_instance
        )  # noqa: E501
        return completed_doses_count + alert_doses_count

    def get_completed_doses_percentage(self, vaccine_protocol_instance):
        completed_doses_count = self.get_completed_doses_count(
            vaccine_protocol_instance
        )
        expected_doses_count = self.get_expected_doses_count(
            vaccine_protocol_instance
        )  # noqa: E501
        try:
            completed_doses_percentage = (
                completed_doses_count / expected_doses_count
            ) * 100
        except ZeroDivisionError:
            completed_doses_percentage = 0

        return round(completed_doses_percentage, 2)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        vaccine_doses = data.get("vaccine_doses", [])

        serialized_vaccine_doses = []
        for vaccine_dose in vaccine_doses:
            vaccine_dose_alerts_count = VaccineDose.get_alerts_count_by_dose(
                dose_id=vaccine_dose["id"]
            )
            completed_amount = VaccineStatus.get_completed_count_by_dose(
                dose=vaccine_dose["id"]
            )
            expected_amount = vaccine_dose_alerts_count + completed_amount
            try:
                completed_dose_percentage = (
                    completed_amount / expected_amount
                ) * 100  # noqa: E501
            except ZeroDivisionError:
                completed_dose_percentage = 0

            vaccine_name = Vaccine.objects.get(
                id=vaccine_dose["vaccine"]
            ).display  # noqa: E501
            vaccine_dose = {
                "id": vaccine_dose["id"],
                "vaccine": {
                    "id": vaccine_dose["vaccine"],
                    "name": vaccine_name,
                },  # noqa: E501
                "dose_order": vaccine_dose["dose_order"],
                "gender_recommendation": vaccine_dose["gender_recommendation"],
                "alerts_count": vaccine_dose_alerts_count,
                "completed_amount": completed_amount,
                "completed_percentage": round(completed_dose_percentage, 2),
            }
            serialized_vaccine_doses.append(vaccine_dose)

        data.update({"vaccine_doses": serialized_vaccine_doses})
        return data
