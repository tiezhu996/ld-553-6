from rest_framework.routers import DefaultRouter
from apps.orders.views import TripOrderViewSet

router = DefaultRouter()
router.register("", TripOrderViewSet, basename="orders")
urlpatterns = router.urls
