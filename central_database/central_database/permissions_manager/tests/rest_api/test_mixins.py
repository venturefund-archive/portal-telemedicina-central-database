from unittest.mock import MagicMock

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase

from central_database.customers.factories import ClientFactory
from central_database.permissions_manager.core import PermissionManager
from central_database.users.tests.factories import UserFactory
from central_database.vaccines.api.serializers import VaccineProtocolSerializer
from central_database.vaccines.models import VaccineProtocol
from central_database.vaccines.tests.factories import VaccineProtocolFactory


class TestPermissionSerializerMixin(APITestCase):
    def setUp(self):
        self.client = ClientFactory()
        self.user = UserFactory(client=self.client)

    def test_it_serializes_object_model_permissions(self):
        Permission.objects.create(
            codename="test_permission_1",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(VaccineProtocol),
        )

        Permission.objects.create(
            codename="test_permission_2",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(VaccineProtocol),
        )

        Permission.objects.create(
            codename="test_permission_3",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(VaccineProtocol),
        )
        ContentType.objects.get_for_model(VaccineProtocol)

        PermissionManager().grant_perm(
            "vaccineprotocol.test_permission_1", self.user
        )  # noqa: E501
        PermissionManager().grant_perm(
            "vaccineprotocol.test_permission_3", self.user
        )  # noqa: E501

        vaccine_protocol = VaccineProtocolFactory(client=self.user.client)

        request_mock = MagicMock()
        request_mock.user = self.user
        VaccineProtocolSerializer.context = {"request": request_mock}
        serialized_vaccine_protocol = VaccineProtocolSerializer(
            vaccine_protocol
        ).data  # noqa: E501

        print(serialized_vaccine_protocol["permissions"])
        self.assertTrue("permissions" in serialized_vaccine_protocol.keys())
        self.assertEqual(
            serialized_vaccine_protocol["permissions"],
            {
                "test_permission_1": {
                    "model_level": True,
                },
                "test_permission_3": {"model_level": True},
            },
        )
