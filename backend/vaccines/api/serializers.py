from typing import Any
from rest_framework import serializers

from vaccines.models import (
    VaccinationCard,
    Vaccine,
    VaccineDose,
    VaccineProtocol,
    Immunization,
    ImmunizationRecommendation,
)

from rest_framework import serializers

class NonNullSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super().to_representation(instance)
        return {key: value for key, value in result.items() if value is not None}


class VaccineSerializer(NonNullSerializer):  # noqa: E501
    class Meta:
        model = Vaccine
        fields = "__all__"
        read_only = True


class VaccineDosesSerializer(NonNullSerializer):  # noqa: E501
    vaccine = VaccineSerializer()
    class Meta:
        model = VaccineDose
        fields = [
            "id",
            "vaccine",
            "minimum_recommended_age",
            "maximum_recommended_age",
            "dose_order",
            "gender_recommendation",
            "booster",
        ]
        read_only = True

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


class VaccinationCardSerializer(NonNullSerializer):
    class Meta:
        model = VaccinationCard
        fields = "__all__"


class VaccineProtocolSerializer(NonNullSerializer):
    class Meta:
        model = VaccineProtocol
        fields = '__all__'

class ImmunizationRecommendationSerializer(NonNullSerializer):
    vaccine_dose = VaccineDosesSerializer()

    class Meta:
        model = ImmunizationRecommendation
        fields = ['id', 'patient_id', 'date', 'vaccine_dose', 'forecast_status', 'forecast_reason', 'due_date', 'vaccine_dose']


class ImmunizationSerializer(NonNullSerializer):
    recommendation = ImmunizationRecommendationSerializer()

    class Meta:
        model = Immunization
        fields = ['id', 'status', 'occurrence_date', 'primary_source', 'performer', 'recommendation']
