from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from central_database.patients.api.views import PatientsViewSet
from central_database.users.api.views import UserViewSet
from central_database.vaccines.api.views import (  # noqa: E501
    VaccineDosesViewSet,
    VaccineViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register("patients", PatientsViewSet, basename="patients")
router.register("users", UserViewSet)
router.register(
    "vaccines/doses", VaccineDosesViewSet, basename="vaccine-doses"
)  # noqa: E501
router.register("vaccines", VaccineViewSet, basename="vaccine")
app_name = "api"
urlpatterns = router.urls
