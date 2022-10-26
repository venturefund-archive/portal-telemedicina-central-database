from django.db import models
from django.contrib.auth.models import Permission
from central_database.users.models import User
from typing import Union, Iterable, List, Set
from django.db.models import QuerySet

import logging

logger = logging.getLogger(__name__)


class Role(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)

    permissions = models.ManyToManyField(Permission)
    users = models.ManyToManyField(User)

    def assign_permission(self, permission: Union[Permission, QuerySet[Permission]], user_doing_action: User = None):
        if isinstance(permission, Iterable):
            self.permissions.add(*permission)
            permissions_codenames = [perm.codename for perm in permission]
            permissions_to_log = str(permissions_codenames)
        else:
            self.permissions.add(permission)
            permissions_to_log = permission.codename
        self.save()

        user_identifier = user_doing_action.email if user_doing_action else 'unknown user'
        logger.info(
            f'Role [{self.id}][{self.slug}] - {user_identifier} assigned {permissions_to_log}'
        )

    def has_permission(self, permission_codename: str):
        return permission_codename in self.permissions.all().values_list('codename', flat=True)

    class Meta:
        unique_together = ['slug', 'company']

    def __str__(self):
        return f'{self.name} | {self.slug}'
