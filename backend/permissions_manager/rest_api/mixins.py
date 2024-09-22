from permissions_manager.core import PermissionManager


class PermissionSerializerMixin:
    def to_representation(self, instance):
        serialized_data = super().to_representation(instance)

        if not self.context.get("request"):
            # https://github.com/encode/django-rest-framework/issues/2555
            return serialized_data

        user = self.context["request"].user
        permission_manager = self.context.get("permission_manager")
        if not permission_manager:
            permission_manager = PermissionManager(user)
            self.context.update({"permission_manager": permission_manager})

        instance_class = instance.__class__
        all_model_permissions = permission_manager._get_model_permissions(
            instance_class
        )

        permissions_dict = {}
        for permission_codename in all_model_permissions:
            permission_string = (
                f"{instance_class._meta.app_label}.{permission_codename}"
            )
            has_model_level_permission = (
                permission_manager.has_model_level_perm(  # noqa: E501
                    permission_string, user
                )
            )
            permission_dict = {
                permission_codename: {
                    "model_level": has_model_level_permission,
                }
            }
            if permission_dict[permission_codename]["model_level"]:
                permissions_dict.update(permission_dict)

        serialized_data.update({"permissions": permissions_dict})
        return serialized_data
