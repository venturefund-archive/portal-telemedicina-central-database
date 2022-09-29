from patients.views import PatientViewSet, VaccineStatusViewSet, VaccineViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register("all", PatientViewSet, basename="patients")
router.register("vaccines", VaccineViewSet, basename="vaccines")
router.register("vaccine-status", VaccineStatusViewSet, basename="status")

urlpatterns = router.urls
