from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from central_database.integrations.fhir_resources.patient import PatientDetail, PatientImmunization


class PatientDetailView(APIView):

    def get(self, request, id, format=None):
        patient = PatientDetail(id)
        data = patient.detail
        return Response(data)


class PatientImmunizationView(APIView):

    def get(self, request, id, format=None):
        patient = PatientImmunization(id)
        data = patient.immunization
        return Response(data)
