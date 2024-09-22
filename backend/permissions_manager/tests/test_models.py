from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework.test import APITestCase

from customers.factories import ClientFactory
from permissions_manager.factories import RoleFactory
from permissions_manager.models import Role
from users.models import User
from users.tests.factories import UserFactory
from vaccines.models import Vaccine


class TestRoleModel(APITestCase):
    def test_it_assign_permission_to_role(self):
        permission = Permission.objects.create(
            codename="test_permission",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(Vaccine),
        )

        role = RoleFactory()
        role.assign_permission(permission)

        self.assertEqual(len(role.permissions.all()), 1)

    def test_it_assign_permissions_in_bulk_to_role(self):
        permission_1 = Permission.objects.create(
            codename="test_permission",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(Vaccine),
        )
        permission_2 = Permission.objects.create(
            codename="test_permission_2",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(Vaccine),
        )
        permissions = [permission_1, permission_2]

        role = RoleFactory()
        role.assign_permission(permissions)

        self.assertEqual(len(role.permissions.all()), 2)

    def test_it_removes_permission_from_role(self):
        permission = Permission.objects.create(
            codename="test_permission",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(Vaccine),
        )

        role = RoleFactory()
        role.assign_permission(permission)
        self.assertEqual(len(role.permissions.all()), 1)

        role.remove_permission(permission)
        self.assertEqual(len(role.permissions.all()), 0)

    def test_it_assign_role_to_user(self):
        role = RoleFactory()
        user = UserFactory()

        role.assign_to_user(user)

        self.assertEqual(len(role.users.all()), 1)

    def test_if_it_is_base_role(self):
        role = RoleFactory(client=None)
        self.assertTrue(role.is_base_role)

        role.client = ClientFactory()
        self.assertFalse(role.is_base_role)

    def test_it_does_not_assign_base_role_to_user(self):
        role = RoleFactory(client=None)
        user = UserFactory()

        role.assign_to_user(user)

        self.assertEqual(len(role.users.all()), 0)

    def test_it_gets_base_role(self):
        role = RoleFactory(client=None, slug="test-role")
        self.assertEqual(Role.get_base_role(role.slug).id, role.id)

    def test_it_creates_role_from_base_role(self):
        permission_1 = Permission.objects.create(
            codename="test_permission",
            name="Can perform tests",
            content_type=ContentType.objects.get_for_model(Vaccine),
        )
        permission_2 = Permission.objects.create(
            codename="test_permission_2",
            name="Can perform tests 2",
            content_type=ContentType.objects.get_for_model(Vaccine),
        )
        base_role = RoleFactory(client=None)
        base_role.assign_permission(permission_1)
        base_role.assign_permission(permission_2)

        client = ClientFactory()
        role_from_base_role = base_role.create_role_from_base_role(client)

        self.assertEqual(base_role.permissions.all().count(), 2)
        self.assertEqual(role_from_base_role.permissions.all().count(), 2)
        self.assertEqual(
            role_from_base_role.permissions.all().first(), permission_1
        )  # E501: noqa
        self.assertEqual(role_from_base_role.client, client)

    def test_it_creates_role_with_permissions(self):
        permissions: list[str] = ["add_user", "change_user"]
        slug: str = "test-role"
        name: str = "Test Role"

        role: Role = Role.create_or_get_with_permissions(
            name, slug, permissions
        )  # E501: noqa

        self.assertIsNotNone(role)
        self.assertEqual(role.name, name)
        self.assertEqual(role.slug, slug)
        self.assertSetEqual(
            set(role.permissions.all()),
            set(Permission.objects.filter(codename__in=permissions)),
        )

    def test_it_gets_role_with_permissions(self):
        permissions: list[str] = ["add_user", "change_user"]
        slug: str = "test-role"
        name: str = "Test Role"
        initial_role_count: int = Role.objects.count() + 1

        initial_role: Role = Role.objects.create(name=name, slug=slug)
        initial_role.permissions.set(
            Permission.objects.filter(codename__in=permissions)
        )
        initial_role.save()

        role: Role = Role.create_or_get_with_permissions(
            name, slug, permissions
        )  # E501: noqa

        self.assertIsNotNone(role)
        self.assertEqual(role.name, name)
        self.assertEqual(role.slug, slug)
        self.assertSetEqual(
            set(role.permissions.all()),
            set(Permission.objects.filter(codename__in=permissions)),
        )
        self.assertEqual(Role.objects.count(), initial_role_count)

    def test_it_gets_users_with_permission_by_a_role(self):
        permission = "change_user"

        user = UserFactory(email="user@test.com", is_active=False)

        initial_role = RoleFactory()
        initial_role.permissions.set(
            Permission.objects.filter(codename=permission)
        )  # E501: noqa
        initial_role.assign_to_user(user)
        initial_role.save()

        permission = Permission.objects.filter(codename=permission)[0]
        user_list = User.objects.filter(role__permissions=permission)
        self.assertEqual(user.user_permissions.all().count(), 0)
        self.assertEqual(user_list[0], user)

    def test_it_gets_users_with_permissions(self):
        permission = "change_user"

        user = UserFactory(email="user@test.com", is_active=False)
        user.user_permissions.set(
            Permission.objects.filter(codename=permission)
        )  # E501: noqa
        self.assertEqual(
            user.user_permissions.all()[0],
            Permission.objects.filter(codename=permission)[0],
        )

    def test_it_gets_users_with_permissions_by_all_sources(self):
        permission_tag = "change_user"
        permission = Permission.objects.filter(codename=permission_tag)[0]

        # assign permission to a role with a user
        user = UserFactory(email="user@test.com", is_active=False)

        role = RoleFactory()
        role.permissions.set(
            Permission.objects.filter(codename=permission_tag)
        )  # E501: noqa
        role.assign_to_user(user)
        role.save()

        # assign permission to user
        user_2 = UserFactory(email="user2@test.com", is_active=False)
        user_2.user_permissions.set(
            Permission.objects.filter(codename=permission_tag)
        )  # E501: noqa
        user_2.save()

        users_list = User.objects.filter(
            Q(user_permissions=permission) | Q(role__permissions=permission)
        )
        self.assertEqual(users_list.count(), 2)
        self.assertIn(user, users_list)
        self.assertIn(user_2, users_list)
