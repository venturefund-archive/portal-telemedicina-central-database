from django.apps import AppConfig


class CustomersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "central_database.customers"

    def ready(self):
        import central_database.customers.schema  # noqa
