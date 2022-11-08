from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from central_database.users.api.views import UserViewSet
from central_database.vaccines.api.views import VaccineDosesViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register(
    "vaccines/doses", VaccineDosesViewSet, basename="vaccine-doses"
)  # noqa: E501

app_name = "api"
urlpatterns = router.urls
