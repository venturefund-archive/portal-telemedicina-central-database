from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from customers.api.views import MicroRegionViewSet
from patients.api.views import PatientsViewSet
from users.api.views import UserViewSet
from vaccines.api.views import (  # noqa: E501
    VaccinationCardViewSet,
    VaccineDosesViewSet,
    VaccineProtocolMetricsViewSet,
    VaccineViewSet,
    ImmunizationViewSet,
    ImmunizationRecommendationViewSet
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(
    "vaccine-protocol/metrics",
    VaccineProtocolMetricsViewSet,
    basename="vaccine-alerts-count",
)
router.register("patients", PatientsViewSet, basename="patients")
router.register("users", UserViewSet)
router.register("vaccines/cards", VaccinationCardViewSet, basename="vaccination-cards")
router.register("vaccines/doses", VaccineDosesViewSet, basename="vaccine-doses")
router.register("vaccines", VaccineViewSet, basename="vaccine")
router.register("microregion", MicroRegionViewSet, basename="microregion")
router.register("immunizations", ImmunizationViewSet, basename="immunizations")
router.register("immunization-recommendations", ImmunizationRecommendationViewSet, basename="immunization-recommendations")
app_name = "api"
urlpatterns = router.urls
