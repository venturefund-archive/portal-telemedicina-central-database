from django.contrib.auth import get_user_model
from rest_framework import serializers

from central_database.customers.api.serializers import ClientSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = User
        fields = [
            "username",
            "name",
            "first_name",
            "last_name",
            "url",
            "client",
        ]  # noqa: E501

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }
