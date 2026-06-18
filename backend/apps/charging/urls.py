from rest_framework.routers import DefaultRouter
from apps.charging.views import ChargingPileViewSet

router = DefaultRouter()
router.register("", ChargingPileViewSet, basename="charging-piles")
urlpatterns = router.urls
