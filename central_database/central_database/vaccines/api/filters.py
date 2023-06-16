from django_filters import rest_framework as filters

from central_database.vaccines.models import Vaccine, VaccineDose


class VaccineFilterSet(filters.FilterSet):
    system = filters.ChoiceFilter(choices=Vaccine.SYSTEM_VALUE_SETS)

    class Meta:
        model = Vaccine
        fields = ["system"]


class VaccineDoseFilterSet(filters.FilterSet):
    class Meta:
        model = VaccineDose
        fields = ["vaccine"]
