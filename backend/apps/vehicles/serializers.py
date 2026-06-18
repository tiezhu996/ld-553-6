from rest_framework import serializers

from apps.users.serializers import UserSerializer
from apps.vehicles.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    driver_detail = UserSerializer(source="driver", read_only=True)

    class Meta:
        model = Vehicle
        fields = "__all__"
