from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.charging.views import ChargingPileViewSet
from apps.common.views import AuditLogViewSet, health
from apps.maintenance.views import MaintenanceRecordViewSet
from apps.orders.views import TripOrderViewSet
from apps.users.views import LoginView, UserViewSet
from apps.vehicles.views import VehicleViewSet

router = DefaultRouter()
router.register("vehicles", VehicleViewSet, basename="vehicles")
router.register("charging-piles", ChargingPileViewSet, basename="charging-piles")
router.register("orders", TripOrderViewSet, basename="orders")
router.register("maintenance-records", MaintenanceRecordViewSet, basename="maintenance-records")
router.register("users", UserViewSet, basename="users")
router.register("audit-logs", AuditLogViewSet, basename="audit-logs")

urlpatterns = [
    path("health/", health),
    path("api/auth/login/", LoginView.as_view()),
    path("api/dashboard/", include("apps.dashboard.urls")),
    path("api/", include(router.urls)),
]
