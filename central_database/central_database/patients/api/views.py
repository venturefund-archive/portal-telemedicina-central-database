import threading
import urllib

from django.core.cache import cache
from django.db.models.query import QuerySet
from fhirclient import client
from fhirclient.models.patient import Patient
from rest_framework import status
from rest_framework.mixins import (  # noqa: E501
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from central_database.integrations.fhir_api.google_fhir import (
    GoogleFHIRClient,
    server_settings,
)
from central_database.patients.api.serializers import PatientSerializer
from central_database.patients.models import PatientProxy
from central_database.permissions_manager.rest_api.permission_classes import (
    permission_class_assembler,
)

_fhir_client_local = threading.local()


def invalidate_cache(callback):
    def wrapper(*args, **kwargs):
        response = callback(*args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            client_city = args[
                1
            ].user.client.city  # assume the request is the first argument
            cache_key = f"patients-{client_city}"
            cache.delete(cache_key)
        return response

    return wrapper


class PatientsViewSet(
    GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
):

    serializer_class = PatientSerializer
    fhir_client_class = GoogleFHIRClient

    permission_classes = [
        IsAuthenticated,
        permission_class_assembler(
            permissions_to_check={
                "list": ["patients.view_patient"],
                "retrieve": ["patients.view_patient"],
                "update": ["patients.change_patient"],
                "partial_update": ["patients.change_patient"],
            }
        ),
    ]

    def get_serializer_context(self):
        context = {
            "request": self.request,
            "format": self.format_kwarg,
            "view": self,
            "method": self.request.method,
        }
        return context

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)

        if request.user.is_authenticated:
            client = request.user.client

            if not hasattr(_fhir_client_local, "fhir_client"):
                _fhir_client_local.fhir_client = self._get_fhir_client(client)

            self.fhir_client = _fhir_client_local.fhir_client
            request.fhir_client = self.fhir_client

        return request

    def _get_fhir_client(self, client):
        settings = server_settings(
            client.fhir_store.dataset, client.fhir_store.fhir_store_id
        )
        return self.fhir_client_class(settings=settings)

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = self.kwargs[lookup_url_kwarg]
        try:
            return Patient.read(filter_kwargs, self.fhir_client.server)
        except client.FHIRNotFoundException:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def extract_page_token(self, url):
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        return query_params.get("_page_token", [None])[0]

    def get_queryset(self) -> QuerySet:
        return PatientProxy.objects.none()

    def list(self, request):
        client_city = self.request.user.client.city
        cache_key = f"patients-{client_city}"

        queryset = cache.get(cache_key)

        if queryset is None:
            search = Patient.where(
                struct={"address-city": client_city, "_count": "1000"}
            )

            queryset_bundle = self.fhir_client.fetch_all_pages(search)

            queryset = [
                entry.resource
                for bundle in queryset_bundle
                for entry in bundle.entry  # noqa: E501
            ]

            cache.set(cache_key, queryset, timeout=3600 * 24)

        serializer = self.get_serializer(queryset, many=True)

        serializer_data = serializer.data

        response = Response(serializer_data)

        return response

    @invalidate_cache
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )  # noqa: E501
        if serializer.is_valid():
            updated_patient = serializer.save()
            updated_patient.update(self.fhir_client.server)

            updated_serializer = self.get_serializer(updated_patient)
            return Response(updated_serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )  # noqa: E501
