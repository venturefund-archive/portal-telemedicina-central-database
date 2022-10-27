from rest_framework import serializers

from central_database.vaccines.models import VaccineAlert, VaccineDose


class VaccineAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineAlert
        fields = "__all__"


class VaccineDosesSerializer(serializers.ModelSerializer):
    alerts = serializers.SerializerMethodField()

    class Meta:
        model = VaccineDose
        fields = [
            "vaccine",
            "minimum_recommended_age",
            "maximum_recommended_age",
            "dose_order",
            "gender_recommendation",
            "alerts",
        ]

    def get_alerts(self, vaccine_dose_instance):
        patient_id = self.context.get("patient_id")
        alerts = vaccine_dose_instance.get_vaccine_alerts(
            patient_id=patient_id
        )  # noqa: E501
        return VaccineAlertSerializer(alerts, many=True).data
