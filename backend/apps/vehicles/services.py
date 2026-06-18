from apps.common.constants.enums import VehicleStatus
from apps.common.exceptions import BusinessException
from apps.vehicles.models import Vehicle


class VehicleService:
    @staticmethod
    def approve(vehicle: Vehicle) -> Vehicle:
        if vehicle.status != VehicleStatus.PENDING:
            raise BusinessException("只有待审核车辆可以审核")
        vehicle.status = VehicleStatus.OPERATING
        vehicle.save(update_fields=["status", "updated_at"])
        return vehicle

    @staticmethod
    def assign_driver(vehicle: Vehicle, driver_id: int) -> Vehicle:
        vehicle.driver_id = driver_id
        vehicle.save(update_fields=["driver", "updated_at"])
        return vehicle

    @staticmethod
    def mark_maintenance(vehicle: Vehicle) -> Vehicle:
        if vehicle.status != VehicleStatus.OPERATING:
            raise BusinessException("只有运营中车辆可以进入维修")
        vehicle.status = VehicleStatus.MAINTENANCE
        vehicle.save(update_fields=["status", "updated_at"])
        return vehicle

    @staticmethod
    def disable(vehicle: Vehicle) -> Vehicle:
        vehicle.status = VehicleStatus.DISABLED
        vehicle.save(update_fields=["status", "updated_at"])
        return vehicle
