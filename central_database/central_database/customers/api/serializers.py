from rest_framework_gis import serializers

from central_database.customers.models import MicroRegion


class MicroRegionSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = MicroRegion
        fields = "__all__"
        geo_field = "polygon"
