from rest_framework import status, views
from rest_framework.response import Response


class HealthCheck(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)
