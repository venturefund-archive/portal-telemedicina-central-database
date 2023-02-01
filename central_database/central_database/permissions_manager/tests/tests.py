import rules
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase

from central_database.customers.factories import ClientFactory
from central_database.permissions_manager.core import PermissionManager
from central_database.permissions_manager.factories import RoleFactory
from central_database.users.tests.factories import UserFactory
from central_database.vaccines.models import Vaccine


class PermissionManagerTestCase(APITestCase):
    def setUp(self):
        self.client = ClientFactory()
        self.user = UserFactory(client=self.client)

    def test_it_check_user_has_permission(self):
        Permission.objects.create(
            codename="test_permission",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(Vaccine),
        )

        PermissionManager().grant_perm("vaccines.test_permission", self.user)

        self.assertTrue(
            PermissionManager().has_perm("vaccines.test_permission", self.user)
        )

    def test_it_checks_the_user_has_permission_through_role(self):
        Permission.objects.create(
            codename="test_permission",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(Vaccine),
        )

        role = RoleFactory(client=self.client)
        role.assign_to_user(self.user)
        PermissionManager().grant_perm("vaccine.test_permission", role)

        self.assertTrue(
            PermissionManager().has_perm("vaccine.test_permission", self.user)
        )

    def test_it_checks_the_user_has_permission_through_custom_rule(self):
        test_user = self.user

        @rules.predicate
        def custom_rule_predicate(user):
            return user == test_user

        rules.add_rule("test_permission_custom_rule", custom_rule_predicate)

        self.assertTrue(
            PermissionManager().has_perm(
                "custom_rule.test_permission_custom_rule", self.user
            )
        )


class PermissionManagerGetPermissionsTestCase(APITestCase):
    def setUp(self):
        self.client = ClientFactory()
        self.user = UserFactory(client=self.client)

    def test_it_lists_user_permission(self):
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

        Permission.objects.create(
            codename="test_permission_4",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(Vaccine),
        )

        role = RoleFactory(client=self.client)
        role.assign_to_user(self.user)

        PermissionManager().grant_perm("vaccine.test_permission_1", self.user)
        PermissionManager().grant_perm("vaccine.test_permission_2", self.user)
        PermissionManager().grant_perm("vaccine.test_permission_3", role)

        user_permissions = PermissionManager(self.user).get_permissions()

        self.assertEqual(
            user_permissions,
            ["test_permission_1", "test_permission_2", "test_permission_3"],
        )
