"""
ASGI config for Central Database project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""
import os
import sys
from pathlib import Path

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

from . import consumers

# This allows easy placement of apps within the interior
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(
            [
                re_path(
                    r"ws/notifications/(?P<room_code>\w+)/$",
                    consumers.SomeConsumer.as_asgi(),
                )
            ]
        ),
    }
)
