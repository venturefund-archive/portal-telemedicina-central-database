from django_filters import rest_framework as filters

from vaccines.models import Vaccine, VaccineDose, Immunization, ImmunizationRecommendation


class VaccineFilterSet(filters.FilterSet):
    class Meta:
        model = Vaccine
        fields = ["system"]


class VaccineDoseFilterSet(filters.FilterSet):
    class Meta:
        model = VaccineDose
        fields = ["vaccine"]

class ImmunizationFilterSet(filters.FilterSet):
    patient_id = filters.CharFilter(field_name='patient_id', lookup_expr='exact')

    class Meta:
        model = Immunization
        fields = ["patient_id"]

class ImmunizationRecommendationFilterSet(filters.FilterSet):
    patient_id = filters.CharFilter(field_name='patient_id', lookup_expr='exact')

    class Meta:
        model = ImmunizationRecommendation
        fields = ["patient_id"]
