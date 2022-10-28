from rest_framework import routers

from central_database.vaccines.views import VaccineDosesViewSet

router = routers.DefaultRouter()
router.register("doses", VaccineDosesViewSet, basename="vaccine-doses")

urlpatterns = router.urls
