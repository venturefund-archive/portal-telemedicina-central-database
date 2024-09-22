from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from permissions_manager.models import Role

admin.site.register(Role)


class InvalidObjectSelection(Exception):
    pass


@admin.action(description="Duplicate and Edit object")
def duplicate_and_edit_object(modeladmin, request, queryset):
    try:
        if queryset.count() != 1:
            raise InvalidObjectSelection

        model = queryset.model
        duplicated_object = model.make_valid_duplicate(
            original=queryset.first()
        )  # noqa: E501

        app_label = model.__module__.rsplit(".")[0]
        model_name = model.__name__.lower()
        view_name = f"admin:{app_label}_{model_name}_change"

        change_url = reverse(view_name, args=(duplicated_object.id,))
        return HttpResponseRedirect(change_url)

    except InvalidObjectSelection:
        modeladmin.message_user(
            request,
            "Invalid Selection. Please select exactly one object",
            messages.ERROR,
        )

    except AttributeError:
        modeladmin.message_user(
            request,
            "The model does not have the make_valid_duplicate implemented",
            messages.ERROR,
        )


admin.site.add_action(duplicate_and_edit_object, "duplicate_and_edit_object")
