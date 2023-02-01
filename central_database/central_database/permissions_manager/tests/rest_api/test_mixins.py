from unittest.mock import MagicMock

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase

from central_database.customers.factories import ClientFactory
from central_database.permissions_manager.core import PermissionManager
from central_database.users.tests.factories import UserFactory
from central_database.vaccines.api.serializers import VaccineSerializer
from central_database.vaccines.models import Vaccine
from central_database.vaccines.tests.factories import VaccineFactory


class TestPermissionSerializerMixin(APITestCase):
    def setUp(self):
        self.client = ClientFactory()
        self.user = UserFactory(client=self.client)

    def test_it_serializes_object_model_permissions(self):
        Permission.objects.create(
            codename="test_permission_1",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(Vaccine),
        )

        Permission.objects.create(
            codename="test_permission_2",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(Vaccine),
        )

        Permission.objects.create(
            codename="test_permission_3",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(Vaccine),
        )
        ContentType.objects.get_for_model(Vaccine)

        PermissionManager().grant_perm("vaccine.test_permission_1", self.user)
        PermissionManager().grant_perm("vaccine.test_permission_3", self.user)

        vaccine = VaccineFactory()

        request_mock = MagicMock()
        request_mock.user = self.user
        VaccineSerializer.context = {"request": request_mock}
        serialized_vaccine = VaccineSerializer(vaccine).data

        print(serialized_vaccine["permissions"])
        self.assertTrue("permissions" in serialized_vaccine.keys())
        self.assertEqual(
            serialized_vaccine["permissions"],
            {
                "test_permission_1": {
                    "model_level": True,
                },
                "test_permission_3": {"model_level": True},
            },
        )
