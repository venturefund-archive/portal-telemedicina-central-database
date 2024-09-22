from fhirclient.models.fhirdate import FHIRDate
from patients.models import Patient, Address
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['line', 'city', 'state', 'postal_code', 'country', 'latitude', 'longitude']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['line'] is not None:
            ret['line'] = [item.strip() for item in ret['line'].split(',')]
        else:
            ret['line'] = []
        return ret

    def to_internal_value(self, data):
        if 'line' in data and isinstance(data['line'], list):
            data['line'] = ', '.join(data['line'])
        return super().to_internal_value(data)


class PatientSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Patient
        fields = ['fhir_id', 'given_name', 'family_name', 'full_name', 'birth_date', 'gender', 'phone', 'email', 'marital_status', 'address']

    def validate(self, data):
        if data.get('full_name') is None and (data.get('given_name') or data.get('family_name')):
            given = ' '.join(data.get('given_name', [])) if data.get('given_name') else ''
            family = data.get('family_name', '') or ''
            data['full_name'] = f"{given} {family}".strip()
        return data


class PatientMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['fhir_id', 'given_name', 'family_name', 'address_line', 'city', 'state', 'postal_code', 'country', 'latitude', 'longitude']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = f"{' '.join(data['given_name'] or [])} {data['family_name'] or ''}".strip()
        return data