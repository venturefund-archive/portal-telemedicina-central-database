from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from rest_framework_gis.fields import GeometryField


class GeoJsonFieldExtension(OpenApiSerializerFieldExtension):
    target_class = GeometryField

    def map_serializer_field(self, auto_schema, direction):
        return {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": [
                        "Point",
                        "Polygon",
                        "LineString",
                        "MultiPoint",
                        "MultiPolygon",
                        "MultiLineString",
                    ],
                },
                "coordinates": {
                    "type": "array",
                    "items": {"type": "array", "items": {"type": "number"}},
                },
            },
            "required": ["type", "coordinates"],
        }
