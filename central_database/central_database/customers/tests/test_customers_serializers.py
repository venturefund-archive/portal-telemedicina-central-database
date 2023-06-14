from rest_framework.test import APITestCase

from central_database.customers.api.serializers import MicroRegionSerializer
from central_database.customers.factories import (  # noqa: E501
    ClientFactory,
    MicroRegionFactory,
)
from central_database.customers.models import MicroRegion


class TestMicroRegionSerializer(APITestCase):
    def test_it_serializes_microregion(self):
        client = ClientFactory()
        microregion = MicroRegionFactory(client=client)

        serialized_microregion = MicroRegionSerializer(microregion).data

        self.assertEqual(serialized_microregion["id"], microregion.id)
        self.assertEqual(
            [list(pair) for pair in microregion.polygon.coords[0]],
            serialized_microregion["geometry"]["coordinates"][0],
        )
        self.assertEqual(
            serialized_microregion["properties"]["name"], microregion.name
        )  # noqa: E501
        self.assertEqual(
            serialized_microregion["properties"]["client"],
            microregion.client.id,  # noqa: E501
        )

    def test_it_serializes_microregion_list(self):
        client = ClientFactory()
        microregion1 = MicroRegionFactory(client=client)
        microregion2 = MicroRegionFactory(client=client)
        microregions = MicroRegion.objects.all()

        serialized_microregions = MicroRegionSerializer(
            microregions, many=True
        ).data  # noqa: E501

        self.assertEqual(serialized_microregions["type"], "FeatureCollection")

        self.assertEqual(len(serialized_microregions["features"]), 2)

        for feature, microregion in zip(
            serialized_microregions["features"], [microregion1, microregion2]
        ):
            self.assertEqual(feature["id"], microregion.id)
            self.assertEqual(
                [list(pair) for pair in microregion.polygon.coords[0]],
                feature["geometry"]["coordinates"][0],
            )
            self.assertEqual(feature["properties"]["name"], microregion.name)
            self.assertEqual(
                feature["properties"]["client"], microregion.client.id
            )  # noqa: E501
