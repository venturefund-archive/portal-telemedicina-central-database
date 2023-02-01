from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate


class VaccinesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "central_database.vaccines"

    def ready(self) -> None:
        post_migrate.connect(create_healthcare_manager_role, sender=self)


def create_healthcare_manager_role(sender, **kwargs):
    Role = apps.get_model("permissions_manager", "Role")

    Role.create_or_get_with_permissions(
        "Healthcare Manager",
        "healthcare-manager",
        ["view_vaccine", "view_vaccinedose"],  # noqa: E501
    )
