from rest_framework.routers import DefaultRouter
from apps.maintenance.views import MaintenanceRecordViewSet

router = DefaultRouter()
router.register("", MaintenanceRecordViewSet, basename="maintenance-records")
urlpatterns = router.urls
