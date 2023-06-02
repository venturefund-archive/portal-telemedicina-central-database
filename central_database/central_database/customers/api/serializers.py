from django.contrib.gis.db import models as gis_models
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from rest_framework_gis.fields import GeometryField

from central_database.customers.models import Client, MicroRegion


class MicroRegionSerializer(gis_serializers.GeoFeatureModelSerializer):
    polygon = gis_models.PolygonField(
        help_text="The GeoJSON representation of the polygon"
    )

    class Meta:
        model = MicroRegion
        fields = "__all__"
        geo_field = "polygon"


FeatureSerializer = inline_serializer(
    name="Feature",
    fields={
        "id": serializers.IntegerField(),
        "type": serializers.CharField(default="Feature"),
        "geometry": GeometryField(),
        "properties": inline_serializer(
            name="Properties",
            fields={
                "name": serializers.CharField(),
                "client": serializers.PrimaryKeyRelatedField(
                    queryset=Client.objects.all()
                ),
            },
        ),
    },
)

FeatureCollectionSerializer = inline_serializer(
    name="FeatureCollection",
    fields={
        "type": serializers.CharField(default="FeatureCollection"),
        "features": serializers.ListField(child=FeatureSerializer),
    },
)
