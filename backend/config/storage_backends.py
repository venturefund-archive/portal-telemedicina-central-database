"""
GoogleCloudStorage extensions suitable for handing Django's
Static and Media files.

Requires following settings:
MEDIA_URL, GS_MEDIA_BUCKET_NAME
STATIC_URL, GS_STATIC_BUCKET_NAME

In addition to
https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
"""
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting


class GoogleCloudMediaStorage(GoogleCloudStorage):
    """GoogleCloudStorage suitable for Django's Media files."""

    def __init__(self, *args, **kwargs):
        if not settings.MEDIA_URL:
            raise Exception("MEDIA_URL has not been configured")
        kwargs["bucket_name"] = setting("GS_MEDIA_BUCKET_NAME")
        super().__init__(*args, **kwargs)

    def url(self, name):
        """.url that doesn't call Google."""
        folder = (
            settings.GS_LOCATION + "/" if settings.GS_LOCATION != "" else ""
        )  # noqa: E501
        return settings.MEDIA_URL + folder + name

    def path(self, name):
        return self.url(name)


class GoogleCloudStaticStorage(GoogleCloudStorage):
    """GoogleCloudStorage suitable for Django's Static files"""

    def __init__(self, *args, **kwargs):
        if not settings.STATIC_URL:
            raise Exception("STATIC_URL has not been configured")
        kwargs["bucket_name"] = setting("GS_STATIC_BUCKET_NAME")
        super().__init__(*args, **kwargs)

    def url(self, name):
        """.url that doesn't call Google."""
        folder = (
            settings.GS_LOCATION + "/" if settings.GS_LOCATION != "" else ""
        )  # noqa: E501
        return settings.STATIC_URL + folder + name
