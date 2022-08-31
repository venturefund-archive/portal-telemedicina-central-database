from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class Health(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response(None, status.HTTP_200_OK)
