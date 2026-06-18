from rest_framework import serializers

from apps.orders.models import TripOrder
from apps.vehicles.serializers import VehicleSerializer


class TripOrderSerializer(serializers.ModelSerializer):
    vehicle_detail = VehicleSerializer(source="vehicle", read_only=True)

    class Meta:
        model = TripOrder
        fields = "__all__"
        read_only_fields = ["order_no"]
