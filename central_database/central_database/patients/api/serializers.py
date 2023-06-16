from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.patient import Patient
from rest_framework import serializers
from rest_framework.serializers import ListSerializer

from central_database.patients.helpers import calculate_age_in_days
from central_database.vaccines.models import VaccineAlert, VaccineProtocol


class FHIRDateField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, FHIRDate):
            return value.date.isoformat()
        return None

    def to_internal_value(self, data):
        if data:
            return FHIRDate(data)
        return None


class AddressSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    line = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True
    )
    city = serializers.CharField(required=False, allow_null=True)
    state = serializers.CharField(required=False, allow_null=True)
    postal_code = serializers.CharField(
        source="postalCode", required=False, allow_null=True
    )
    country = serializers.CharField(required=False, allow_null=True)
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    def get_latitude(self, obj):
        return self.get_coordinate_value(obj, "latitude")

    def get_longitude(self, obj):
        return self.get_coordinate_value(obj, "longitude")

    def get_coordinate_value(self, obj, coordinate_name):
        if obj.extension:
            for inner_ext in obj.extension[0].extension:
                if inner_ext.url == coordinate_name:
                    return inner_ext.valueDecimal
        return None


class PatientListSerializer(ListSerializer):
    def to_representation(self, data):
        instances = super().to_representation(data)
        keys_to_remove = ["telecom", "gender", "marital_status"]
        client = self.context.get("request").user.client
        protocol = VaccineProtocol.get_vaccine_protocol_by_client(
            client_id=client
        )  # noqa: E501
        alerts = protocol.get_number_of_doses_with_alerts_by_patient()

        patient_ids = [instance["id"] for instance in instances]
        all_alerts = VaccineAlert.get_alerts_by_patient(patient_ids)

        updated_instances = [
            {
                **{
                    k: v
                    for k, v in instance.items()
                    if k not in keys_to_remove  # noqa: E501
                },
                "number_of_alerts_by_protocol": alerts.get(instance["id"], 0),
                "age_in_days": calculate_age_in_days(instance["birth_date"]),
                "alerts": all_alerts.get(instance["id"], []),
                "address": {
                    "latitude": instance["address"][0]["latitude"],
                    "longitude": instance["address"][0]["longitude"],
                },
            }
            for instance in instances
        ]

        return sorted(
            updated_instances,
            key=lambda x: (
                -x["number_of_alerts_by_protocol"],
                x["age_in_days"],
            ),  # noqa: E501
        )


class PatientSerializer(serializers.Serializer):
    resource_type = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)
    birth_date = FHIRDateField(source="birthDate")
    name = serializers.SerializerMethodField(source="name")
    gender = serializers.CharField(allow_null=True)
    telecom = serializers.CharField(allow_null=True)
    marital_status = serializers.CharField(
        source="maritalStatus", allow_null=True
    )  # noqa: E501
    address = serializers.SerializerMethodField(source="address")

    def create(self, validated_data):
        return Patient(validated_data)

    def to_internal_value(self, data):
        deserialized_data = super().to_internal_value(data)

        if "name" in data:
            deserialized_data["name"] = data["name"]
        if "address" in data:
            deserialized_data["address"] = data["address"]

        return deserialized_data

    def validate(self, data):
        method = self.context.get("method", False)

        if method == "PUT":
            if "name" not in data or not data["name"]:
                raise serializers.ValidationError(
                    {"name": "This field is required."}
                )  # noqa: E501

            if "address" not in data or not data["address"]:
                raise serializers.ValidationError(
                    {"address": "This field is required."}
                )

        if method == "PATCH":
            if "address" in data:
                for address in data["address"]:
                    if "id" not in address or not address["id"]:
                        raise serializers.ValidationError(
                            {"id": "This field is required."}
                        )

        return data

    def update(self, instance, validated_data):
        if "birth_date" in validated_data:
            instance.birthDate = FHIRDate(validated_data["birth_date"])

        if "name" in validated_data:
            for human_name in instance.name:
                name = validated_data["name"].split()
                human_name.given = name[:-1]
                human_name.family = name[-1]
                human_name.text = validated_data["name"]

        if "gender" in validated_data:
            instance.gender = validated_data["gender"]

        if "telecom" in validated_data:
            instance.telecom = validated_data["telecom"]

        if "marital_status" in validated_data:
            instance.maritalStatus = CodeableConcept.construct(
                text=validated_data["marital_status"]
            )

        if "address" in validated_data:
            for address_data in validated_data["address"]:
                address_instance = instance.address[address_data.pop("id") - 1]
                latitude = address_data.pop("latitude", None)
                longitude = address_data.pop("longitude", None)

                if latitude is not None or longitude is not None:
                    if address_instance.extension is None:
                        raise serializers.ValidationError(
                            {
                                "detail": "The resource doesn't have a coordinate extension configured. Please check the fhirStore"  # noqa: E501
                            }
                        )

                    for nested_extension in address_instance.extension:
                        if nested_extension.extension is None:
                            raise serializers.ValidationError(
                                {
                                    "detail": "The resource doesn't have a coordinate extension configured. Please check the fhirStore"  # noqa: E501
                                }
                            )

                        for ext in nested_extension.extension:
                            if ext.url == "latitude":
                                ext.valueDecimal = latitude
                            elif ext.url == "longitude":
                                ext.valueDecimal = longitude

                for key, value in address_data.items():
                    setattr(address_instance, key, value) if hasattr(
                        address_instance, key
                    ) else None

        return instance

    def get_name(self, obj):
        if obj.name and len(obj.name) > 0:
            name = obj.name[0]
            parts = []
            if name.given:
                parts.extend(name.given)
            if name.family:
                parts.append(name.family)
            return " ".join(parts)
        return None

    def get_address(self, obj):
        if obj.address:
            for index, address in enumerate(obj.address):
                address.id = index + 1
            return AddressSerializer(obj.address, many=True).data
        return []

    class Meta:
        list_serializer_class = PatientListSerializer
