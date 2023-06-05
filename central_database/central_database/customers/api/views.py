from drf_spectacular.utils import extend_schema
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from central_database.customers.api.serializers import (
    FeatureCollectionSerializer,
    FeatureSerializer,
    MicroRegionSerializer,
)
from central_database.customers.models import MicroRegion


def extend_schema_microregion():
    return extend_schema(
        request=MicroRegionSerializer,
        responses={200: FeatureSerializer},
    )


class MicroRegionViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    serializer_class = MicroRegionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        client = self.request.user.client
        return MicroRegion.get_for_client(client)

    @extend_schema(
        request=MicroRegionSerializer,
        responses={
            200: FeatureCollectionSerializer,
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema_microregion()
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema_microregion()
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema_microregion()
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema_microregion()
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
