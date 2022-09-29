from patients.models import Patient, Vaccine, VaccineStatus
from rest_framework import serializers


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = "__all__"


class VaccineStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineStatus
        fields = "__all__"
