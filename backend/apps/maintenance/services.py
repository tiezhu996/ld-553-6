from django.utils import timezone

from apps.common.constants.enums import VehicleStatus
from apps.maintenance.models import MaintenanceRecord


class MaintenanceService:
    @staticmethod
    def create_record(serializer) -> MaintenanceRecord:
        record = serializer.save(status=MaintenanceRecord.Status.IN_PROGRESS)
        record.vehicle.status = VehicleStatus.MAINTENANCE
        record.vehicle.save(update_fields=["status", "updated_at"])
        return record

    @staticmethod
    def complete(record: MaintenanceRecord) -> MaintenanceRecord:
        record.status = MaintenanceRecord.Status.COMPLETED
        record.end_date = timezone.now().date()
        record.save(update_fields=["status", "end_date"])
        record.vehicle.status = VehicleStatus.OPERATING
        record.vehicle.save(update_fields=["status", "updated_at"])
        return record
