from rest_framework import serializers

from apps.maintenance.models import MaintenanceRecord


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    plate_number = serializers.CharField(source="vehicle.plate_number", read_only=True)

    class Meta:
        model = MaintenanceRecord
        fields = "__all__"
