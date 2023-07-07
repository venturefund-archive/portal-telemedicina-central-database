import threading
import urllib

from django.urls import reverse
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
from central_database.permissions_manager.rest_api.permission_classes import (
    permission_class_assembler,
)

_fhir_client_local = threading.local()


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

    def get_queryset(self):
        page_token = self.request.query_params.get("page_token", None)
        client_city = self.request.user.client.city
        if page_token:
            search = Patient.where(
                struct={
                    "address-city": client_city,
                    "_page_token": page_token,
                    "_count": "1000",
                }
            )
        else:
            search = Patient.where(
                struct={"address-city": client_city, "_count": "1000"}
            )

        resources = []
        queryset_bundle, next_url = self.fhir_client.fetch_page(search)
        next_page_token = (
            self.extract_page_token(next_url) if next_url else None
        )  # noqa: E501
        if next_page_token:
            api_next_url = (
                self.request.build_absolute_uri(reverse("api:patients-list"))
                + f"?page_token={next_page_token}"
            )
        else:
            api_next_url = None
        resources.extend(queryset_bundle.entry)

        return [entry.resource for entry in resources], api_next_url

    def list(self, request):
        queryset, next_url = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"results": serializer.data, "next_url": next_url})

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
