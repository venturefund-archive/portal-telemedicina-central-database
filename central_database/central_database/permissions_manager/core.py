import logging
import uuid
from typing import Union

import rules
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

from central_database.permissions_manager.exceptions import (
    InvalidPermissionCodenameFormat,
)
from central_database.permissions_manager.models import Role
from central_database.users.models import User

logger = logging.getLogger(__name__)


def get_override_rule(permission_codename):
    """
    override rules are used when the usual check flow needs to be supressed
    and the content of a 'override rule' is used instead
    """
    return permission_codename + "_override"


def generate_has_user_permission_predicate(
    permission_string: str,
) -> rules.predicate:  # noqa: E501
    @rules.predicate
    def has_user_permission(user):
        return user.has_perm(permission_string)

    return has_user_permission


def generate_has_role_permission_predicate(
    permission_codename: str,
) -> rules.predicate:  # noqa: E501
    @rules.predicate
    def has_role_permission(user):
        user_permission_codenames = Permission.objects.filter(
            role__users=user
        ).values_list("codename", flat=True)
        user_has_role_permission = (
            permission_codename in user_permission_codenames
        )  # noqa: E501
        return user_has_role_permission

    return has_role_permission


class PermissionManager:
    def __init__(self, user: User = None):
        self.user = user

    @staticmethod
    def _get_permission_codename_from_string(permission_string: str):
        try:
            return permission_string.split(".")[1]
        except IndexError:
            raise InvalidPermissionCodenameFormat

    def grant_perm(self, permission_string: str, target: Union[User, Role]):
        permission_codename = self._get_permission_codename_from_string(
            permission_string
        )
        permission = Permission.objects.get(codename=permission_codename)

        if isinstance(target, User):
            self._grant_permission_to_user(permission_codename, target)
        elif isinstance(target, Role):
            self._grant_permission_to_role(permission, target)

    def _grant_permission_to_user(self, permission_codename: str, user: User):
        user_identifier = self.user.email if self.user else "unknown"
        permission = Permission.objects.get(codename=permission_codename)
        user.user_permissions.add(permission)

        logger.info(
            f"PermissionManager - {user_identifier} assigned permission \
            {permission_codename} to {user.email}"
        )

    def _grant_permission_to_role(self, permission: Permission, role: Role):
        role.assign_permission(permission, self.user)

    def revoke_perm(self, permission_string: str, target: Union[User, Role]):
        permission_codename = self._get_permission_codename_from_string(
            permission_string
        )
        permission = Permission.objects.get(codename=permission_codename)

        if isinstance(target, User):
            self._revoke_permission_from_user(permission_codename, target)
        elif isinstance(target, Role):
            self._revoke_permission_from_role(permission, target)

    def _revoke_permission_from_user(
        self, permission_codename: str, user: User
    ):  # noqa: E501
        user_identifier = self.user.email if self.user else "unkown"
        permission = Permission.objects.get(codename=permission_codename)
        user.user_permissions.remove(permission)
        logger.info(
            f"PermissionManager - {user_identifier} revoked \
            {permission_codename} from {user.email}"
        )

    def _revoke_permission_from_role(self, permission: Permission, role: Role):
        role.remove_permission(permission, self.user)

    @staticmethod
    def _get_temporary_rule_name(permission_codename: str):
        return permission_codename + "_" + str(uuid.uuid4()) + "_temp"

    def has_perm(
        self, permission_string: str, user: User, obj: models.Model = None
    ):  # noqa: E501
        if not user.id:
            raise User.DoesNotExist

        permission_codename = self._get_permission_codename_from_string(
            permission_string
        )

        # Override Rule check
        if rules.rule_exists(get_override_rule(permission_codename)):
            return rules.test_rule(
                get_override_rule(permission_codename), user, obj
            )  # noqa: E501

        # Permission Specific Rule check
        if rules.rule_exists(permission_codename) and rules.test_rule(
            permission_codename, user, obj
        ):
            # Only returns if user has permission, otherwise
            # the following permissions are still checked
            return True

        has_user_permission = generate_has_user_permission_predicate(
            permission_string
        )  # noqa: E501
        has_role_permission = generate_has_role_permission_predicate(
            permission_codename
        )

        rule_name = self._get_temporary_rule_name(permission_codename)
        rules.add_rule(
            rule_name,
            has_user_permission | has_role_permission,
        )
        result = rules.test_rule(rule_name, user, obj)
        rules.remove_rule(rule_name)

        return result

    def has_model_level_perm(self, permission_string: str, user: User):
        if not user.id:
            raise User.DoesNotExist

        permission_codename = self._get_permission_codename_from_string(
            permission_string
        )

        # Override Rule check
        if rules.rule_exists(get_override_rule(permission_codename)):
            return rules.test_rule(
                get_override_rule(permission_codename), user
            )  # noqa: E501

        # Permission Specific Rule check
        if rules.rule_exists(permission_codename) and rules.test_rule(
            permission_codename, user
        ):
            # Only returns if user has permission, otherwise
            # the following permissions are still checked
            return True

        has_user_permission = generate_has_user_permission_predicate(
            permission_string
        )  # noqa: E501
        has_role_permission = generate_has_role_permission_predicate(
            permission_codename
        )

        rule_name = self._get_temporary_rule_name(permission_codename)
        rules.add_rule(
            rule_name,
            has_user_permission | has_role_permission,
        )
        result = rules.test_rule(rule_name, user)
        rules.remove_rule(rule_name)

        return result

    def _get_model_permissions(self, model_class: type):
        content_type = ContentType.objects.get_for_model(model_class)
        model_permissions = Permission.objects.filter(
            content_type=content_type
        ).values_list("codename", flat=True)
        return model_permissions

    def get_permissions(
        self, model_class: Union[models.Model, type] = None
    ) -> list[str]:

        permissions_attached_to_user = list(
            self.user.user_permissions.all().values_list("codename", flat=True)
        )
        permissions_attached_to_role = list(
            Permission.objects.filter(role__users=self.user).values_list(
                "codename", flat=True
            )
        )
        all_static_user_permissions = set(
            permissions_attached_to_user + permissions_attached_to_role
        )

        if model_class:
            all_model_permissions = self._get_model_permissions(model_class)

            static_model_level_permissions = (
                all_static_user_permissions.intersection(  # noqa: E501
                    all_model_permissions
                )
            )

            model_level_permissions = list(static_model_level_permissions)
            model_level_permissions.sort()
            return model_level_permissions

        else:
            user_permissions = list(all_static_user_permissions)
            user_permissions.sort()
            return user_permissions
