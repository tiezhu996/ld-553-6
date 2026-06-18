from rest_framework import decorators, response, viewsets

from apps.charging.models import ChargingPile
from apps.charging.serializers import ChargingPileSerializer
from apps.charging.services import ChargingService
from apps.common.constants.enums import PileStatus
from apps.common.permissions import IsOperatorOrAdmin


class ChargingPileViewSet(viewsets.ModelViewSet):
    serializer_class = ChargingPileSerializer
    permission_classes = [IsOperatorOrAdmin]

    def get_queryset(self):
        queryset = ChargingPile.objects.all()
        if pile_type := self.request.query_params.get("type"):
            queryset = queryset.filter(type=pile_type)
        if state := self.request.query_params.get("status"):
            queryset = queryset.filter(status=state)
        return queryset

    def perform_create(self, serializer):
        serializer.save(status=PileStatus.IDLE)

    @decorators.action(detail=False, methods=["get"], url_path="locations")
    def locations(self, request):
        return response.Response(ChargingPileSerializer(self.get_queryset(), many=True).data)

    @decorators.action(detail=True, methods=["patch"], url_path="status")
    def status_action(self, request, pk=None):
        return response.Response(ChargingPileSerializer(ChargingService.set_status(self.get_object(), request.data["status"])).data)

    @decorators.action(detail=True, methods=["patch"], url_path="price")
    def price(self, request, pk=None):
        return response.Response(ChargingPileSerializer(ChargingService.update_price(self.get_object(), request.data["price_per_kwh"])).data)
