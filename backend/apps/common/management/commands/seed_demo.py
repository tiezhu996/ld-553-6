from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.charging.models import ChargingPile
from apps.common.constants.enums import OrderStatus, PaymentStatus, PileStatus, PileType, VehicleStatus, VehicleType
from apps.orders.models import TripOrder
from apps.users.models import User
from apps.vehicles.models import Vehicle


class Command(BaseCommand):
    help = "Seed TransitHub demo users and business data."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(username="admin", defaults={"role": User.Role.ADMIN, "email": "admin@transithub.local"})
        admin.set_password("admin123456")
        admin.save()
        driver, _ = User.objects.get_or_create(username="driver01", defaults={"role": User.Role.DRIVER})
        driver.set_password("driver123456")
        driver.save()
        vehicle, _ = Vehicle.objects.get_or_create(
            plate_number="沪A-TH553",
            defaults={
                "type": VehicleType.RIDE_HAILING,
                "brand": "比亚迪",
                "model": "D1",
                "year": 2024,
                "status": VehicleStatus.OPERATING,
                "driver": driver,
                "insurance_expiry": "2027-06-01",
                "lat": Decimal("31.2304000"),
                "lng": Decimal("121.4737000"),
            },
        )
        ChargingPile.objects.get_or_create(
            code="CP-SH-001",
            defaults={
                "location": "人民广场地下充电站",
                "lat": Decimal("31.2317000"),
                "lng": Decimal("121.4755000"),
                "type": PileType.FAST,
                "power": Decimal("120.00"),
                "status": PileStatus.IDLE,
                "price_per_kwh": Decimal("1.35"),
                "installed_at": timezone.now(),
            },
        )
        TripOrder.objects.get_or_create(
            order_no="THDEMO553001",
            defaults={
                "user": driver,
                "vehicle": vehicle,
                "start_location": "人民广场",
                "end_location": "虹桥枢纽",
                "start_lat": Decimal("31.2304000"),
                "start_lng": Decimal("121.4737000"),
                "end_lat": Decimal("31.1979000"),
                "end_lng": Decimal("121.3201000"),
                "distance": Decimal("18.60"),
                "duration": 42,
                "fare": Decimal("82.00"),
                "status": OrderStatus.COMPLETED,
                "payment_status": PaymentStatus.PAID,
            },
        )
        self.stdout.write(self.style.SUCCESS("TransitHub demo data seeded."))
