import logging
from typing import Optional

from django.contrib import messages
from django.db import models
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request

from permissions_manager.core import PermissionManager

logger = logging.getLogger(__name__)


def authorize(
    request, action: str, error_message: str, is_ajax: bool = False
) -> Optional[HttpResponse]:

    """Checks whether the current user
    has permission to perform the given action,
    returning None if ok.
    If not, the error message will be returned.
    """

    if not PermissionManager().has_perm(action, request.user):
        logger.critical(f"PermissionDenied: {request.user} cannot {action}")
        messages.error(request, error_message)
        return HttpResponse(error_message, status=403)

    return None


def permission_class_assembler(permissions_to_check):
    # permissions_to_check format
    # permissions_to_check = {
    #     '<action>': ['<app>.<codename>', '<app>.<codename>'],
    #     '<action>': ['<app>.<codename>', '<app>.<codename>']
    # }

    class PermissionClass(PermissionBaseClass):
        pass

    PermissionClass.permissions_to_check = permissions_to_check
    return PermissionClass


class PermissionBaseClass(BasePermission):
    def check_permissions(
        self, request: Request, action: str, obj: Optional[models.Model] = None
    ):
        permissions = self.permissions_to_check.get(action)
        if permissions:
            user = request.user
            permissions_manager = PermissionManager(user)
            for permission in permissions:
                if not permissions_manager.has_perm(permission, user, obj):
                    return False
        return True

    def has_permission(self, request: Request, view):
        return self.check_permissions(request, view.action)


class CRUDPermissionClass(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        permission_name: str = view.permission_name
        permission_app: str = view.permission_app
        permission_action: str

        if request.method in ["PUT", "PATCH"]:
            permission_action = "change"
        elif request.method == "POST":
            permission_action = "add"
        elif request.method == "DELETE":
            permission_action = "delete"

        error_response: str = authorize(
            request,
            f"{permission_app}.{permission_action}_{permission_name}",
            f"Not allowed to {permission_action} {permission_name}",
            is_ajax=True,
        )

        if error_response:
            raise ValidationError(
                detail={
                    "error": [
                        f"Not allowed to {permission_action} {permission_name}"
                    ]  # noqa: E501
                },
                code=400,
            )
        else:
            return True
