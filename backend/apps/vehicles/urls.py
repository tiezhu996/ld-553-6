from rest_framework.routers import DefaultRouter
from apps.vehicles.views import VehicleViewSet

router = DefaultRouter()
router.register("", VehicleViewSet, basename="vehicles")
urlpatterns = router.urls
