from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from central_database.customers.api.serializers import MicroRegionSerializer
from central_database.customers.models import MicroRegion


class MicroRegionViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = MicroRegionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        client = self.request.user.client
        return MicroRegion.get_for_client(client)
