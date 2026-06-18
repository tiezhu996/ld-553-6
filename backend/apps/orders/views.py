from rest_framework import decorators, response, viewsets

from apps.common.permissions import IsOperatorOrAdmin
from apps.orders.models import TripOrder
from apps.orders.serializers import TripOrderSerializer
from apps.orders.services import OrderService


class TripOrderViewSet(viewsets.ModelViewSet):
    serializer_class = TripOrderSerializer
    permission_classes = [IsOperatorOrAdmin]

    def get_queryset(self):
        queryset = TripOrder.objects.select_related("user", "vehicle", "vehicle__driver")
        user = self.request.user
        if getattr(user, "role", "") == "DRIVER":
            queryset = queryset.filter(vehicle__driver=user)
        if state := self.request.query_params.get("status"):
            queryset = queryset.filter(status=state)
        if start := self.request.query_params.get("start_date"):
            queryset = queryset.filter(created_at__date__gte=start)
        if end := self.request.query_params.get("end_date"):
            queryset = queryset.filter(created_at__date__lte=end)
        return queryset

    def perform_create(self, serializer):
        OrderService.create_order(serializer, self.request.user)

    @decorators.action(detail=True, methods=["patch"], url_path="status")
    def status_action(self, request, pk=None):
        order = OrderService.set_status(self.get_object(), request.data["status"], request.data.get("vehicle_id"))
        return response.Response(TripOrderSerializer(order).data)

    @decorators.action(detail=True, methods=["patch"])
    def pay(self, request, pk=None):
        return response.Response(TripOrderSerializer(OrderService.pay(self.get_object())).data)
