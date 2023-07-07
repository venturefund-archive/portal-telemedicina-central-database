from typing import Any

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from central_database.customers.api.serializers import (  # noqa: E501
    HealthProfessionalSerializer,
)
from central_database.customers.models import HealthProfessional
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


class VaccineSerializer(serializers.ModelSerializer):  # noqa: E501
    class Meta:
        model = Vaccine
        fields = "__all__"


class VaccineAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineAlert
        fields = "__all__"


class VaccineStatusSerializer(serializers.ModelSerializer):
    health_professional = HealthProfessionalSerializer(
        required=False, allow_null=True
    )  # noqa: E501

    class Meta:
        model = VaccineStatus
        fields = "__all__"

    def create(self, validated_data):
        if VaccineStatus.objects.filter(
            vaccine_dose=validated_data["vaccine_dose"],
            patient_id=validated_data["patient_id"],
        ).exists():
            raise serializers.ValidationError(
                "A status for this dose and patient already exists"
            )

        health_professional_data = validated_data.pop(
            "health_professional", {}
        )  # noqa: E501
        cns_number = health_professional_data.get("cns_number", None)
        health_professional = None
        if cns_number is not None:
            health_professional, _ = HealthProfessional.objects.get_or_create(
                cns_number=cns_number, defaults=health_professional_data
            )  # Creates a new professional only if cns_number doesn't exist
        if health_professional is not None:
            validated_data["health_professional"] = health_professional
        vaccine_status = VaccineStatus.objects.create(**validated_data)
        return vaccine_status

    def update(self, instance, validated_data):
        health_professional_data = validated_data.pop(
            "health_professional", {}
        )  # noqa: E501
        health_professional = None
        if health_professional_data is not None:
            cns_number = health_professional_data.get("cns_number", None)
            if cns_number is not None:
                (
                    health_professional,
                    _,
                ) = HealthProfessional.objects.get_or_create(  # noqa: E501
                    cns_number=cns_number, defaults=health_professional_data
                )
            if health_professional is not None:
                validated_data["health_professional"] = health_professional
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class VaccineDosesSerializer(serializers.ModelSerializer):  # noqa: E501
    alerts = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

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
            "status",
            "booster",
        ]

    @extend_schema_field(VaccineAlertSerializer(many=True))
    def get_alerts(self, vaccine_dose_instance):
        alerts = getattr(vaccine_dose_instance, "active_alerts", None)
        if alerts is not None:
            return VaccineAlertSerializer(alerts, many=True).data
        return None

    @extend_schema_field(VaccineStatusSerializer(many=False))
    def get_status(self, vaccine_dose_instance):
        status = getattr(vaccine_dose_instance, "patient_status", None)
        if status:
            return VaccineStatusSerializer(status[0]).data
        return None

    def remove_keys(self, data_dict, keys_to_remove):
        for key in keys_to_remove:
            data_dict.pop(key, None)

    def to_representation(self, instance: Any) -> Any:
        data = super().to_representation(instance)
        keys_to_remove = ["patient_id", "vaccine_dose"]

        if data.get("status"):
            self.remove_keys(data["status"], keys_to_remove)

        if data.get("alerts"):
            for alert in data["alerts"]:
                self.remove_keys(alert, keys_to_remove)

        return data


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
