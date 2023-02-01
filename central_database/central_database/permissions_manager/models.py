from __future__ import annotations

import copy
import logging
from typing import Iterable

from django.contrib.auth.models import Permission
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from simple_history.models import HistoricalRecords

from central_database.customers.models import Client
from central_database.users.models import User

logger = logging.getLogger(__name__)


class Role(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)

    permissions = models.ManyToManyField(Permission)
    users = models.ManyToManyField(User, blank=True)

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, null=True, blank=True
    )  # E501: noqa

    history = HistoricalRecords()

    def assign_permission(
        self,
        permission: Permission | QuerySet[Permission],
        user_doing_action: User = None,
    ):
        if isinstance(permission, Iterable):
            self.permissions.add(*permission)
            permissions_codenames = [perm.codename for perm in permission]
            permissions_to_log = str(permissions_codenames)
        else:
            self.permissions.add(permission)
            permissions_to_log = permission.codename
        self.save()

        user_identifier = (
            user_doing_action.email if user_doing_action else "unknown user"
        )
        logger.info(
            f"Role [{self.id}][{self.slug}] - {user_identifier} assigned \
                {permissions_to_log}"
        )

    def remove_permission(
        self, permission: Permission, user_doing_action: User = None
    ):  # E501: noqa
        self.permissions.remove(permission)
        user_identifier = (
            user_doing_action.email if user_doing_action else "unknown user"
        )
        logger.info(
            f"Role [{self.id}][{self.slug}] - {user_identifier} \
                removed {permission.codename}"
        )

    def has_permission(self, permission_codename: str):
        return permission_codename in self.permissions.all().values_list(
            "codename", flat=True
        )

    def assign_to_user(self, user: User, user_doing_action: User = None):
        if not self.is_base_role:
            self.users.add(user)
            user_identifier = (
                user_doing_action.email if user_doing_action else "unkown"
            )  # E501: noqa
            logger.info(
                f"Role [{self.id}][{self.slug}] - {user_identifier} \
                     assigned role to user: {user.email}"
            )

    @property
    def is_base_role(self):
        return self.client is None

    def create_role_from_base_role(self, client: Client):
        if self.is_base_role:
            permissions = self.permissions.all()
            new_role = copy.deepcopy(self)
            new_role.pk = None
            new_role.client = client
            new_role.save()
            new_role.assign_permission(permissions)

            return new_role
        return None

    @staticmethod
    def get_base_role(slug: str) -> Role:
        return Role.objects.filter(client__isnull=True).get(slug=slug)

    @staticmethod
    def get_for_client(client: Client) -> models.QuerySet[Role]:
        return Role.objects.filter(Q(client=client) | Q(client__isnull=True))

    @staticmethod
    def create_or_get_with_permissions(
        name: str, slug: str, permissions_codenames: list[str]
    ) -> Role:
        base_role, created = Role.objects.get_or_create(
            slug=slug, name=name, client=None
        )

        # This way it raises error in case a codename is invalid
        permissions: QuerySet[Permission] = Permission.objects.filter(
            codename__in=permissions_codenames
        )
        base_role.permissions.set(list(permissions))

        return base_role

    class Meta:
        unique_together = ["slug", "client"]

    def __str__(self):
        client: str = self.client or "Base"
        return f"{client} | {self.name}"
