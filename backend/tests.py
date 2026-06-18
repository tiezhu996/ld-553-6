from datetime import date
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.charging.models import ChargingPile
from apps.common.constants.enums import PileStatus, PileType, VehicleStatus, VehicleType
from apps.maintenance.models import MaintenanceRecord
from apps.orders.models import TripOrder
from apps.users.models import User
from apps.vehicles.models import Vehicle


def _today():
    return date(2026, 6, 18)


class MaintenanceAccessControlTests(TestCase):
    """
    验收测试：维修入口统一校验（只有运营中车辆可进入维修）

    覆盖两个维修入口：
    A. POST /api/maintenance-records/            创建维修记录入口
    B. PATCH /api/vehicles/{id}/maintenance/     车辆快捷维修入口
    """

    @classmethod
    def setUpTestData(cls):
        cls.operator = User.objects.create_user(
            username="op1", password="p@ssw0rd", role=User.Role.OPERATOR
        )
        cls.vehicle_op = Vehicle.objects.create(
            plate_number="沪A-OP001",
            type=VehicleType.TAXI,
            brand="比亚迪",
            model="e6",
            year=2024,
            status=VehicleStatus.OPERATING,
            insurance_expiry=_today(),
        )
        cls.vehicle_pending = Vehicle.objects.create(
            plate_number="沪A-PD001",
            type=VehicleType.BUS,
            brand="宇通",
            model="Z11",
            year=2023,
            status=VehicleStatus.PENDING,
            insurance_expiry=_today(),
        )
        cls.vehicle_maint = Vehicle.objects.create(
            plate_number="沪A-MT001",
            type=VehicleType.RIDE_HAILING,
            brand="吉利",
            model="几何A",
            year=2024,
            status=VehicleStatus.MAINTENANCE,
            insurance_expiry=_today(),
        )
        cls.vehicle_disabled = Vehicle.objects.create(
            plate_number="沪A-DS001",
            type=VehicleType.LOGISTICS,
            brand="上汽",
            model="大通EV90",
            year=2022,
            status=VehicleStatus.DISABLED,
            insurance_expiry=_today(),
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.operator)

    # ---------------- 入口 A：POST /api/maintenance-records/ ----------------

    def _maintenance_payload(self, vehicle_id):
        return {
            "vehicle": vehicle_id,
            "type": "例行保养",
            "description": "10000公里例行检查",
            "cost": "350.00",
            "start_date": _today().isoformat(),
        }

    def test_A_operating_vehicle_can_create_maintenance_record(self):
        """运营中车辆可以创建维修记录"""
        res = self.client.post(reverse("maintenance-records-list"), self._maintenance_payload(self.vehicle_op.id))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.data)
        self.vehicle_op.refresh_from_db()
        self.assertEqual(self.vehicle_op.status, VehicleStatus.MAINTENANCE)
        record = MaintenanceRecord.objects.filter(vehicle_id=self.vehicle_op.id).first()
        self.assertIsNotNone(record)
        self.assertEqual(record.status, MaintenanceRecord.Status.IN_PROGRESS)

    def test_A_pending_vehicle_rejected(self):
        """待审核车辆无法创建维修记录"""
        res = self.client.post(reverse("maintenance-records-list"), self._maintenance_payload(self.vehicle_pending.id))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.vehicle_pending.refresh_from_db()
        self.assertEqual(self.vehicle_pending.status, VehicleStatus.PENDING)
        self.assertFalse(MaintenanceRecord.objects.filter(vehicle_id=self.vehicle_pending.id).exists())

    def test_A_maintenance_vehicle_rejected(self):
        """已在维修车辆无法重复创建维修记录"""
        res = self.client.post(reverse("maintenance-records-list"), self._maintenance_payload(self.vehicle_maint.id))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.vehicle_maint.refresh_from_db()
        self.assertEqual(self.vehicle_maint.status, VehicleStatus.MAINTENANCE)

    def test_A_disabled_vehicle_rejected(self):
        """停用/报废车辆无法创建维修记录"""
        res = self.client.post(reverse("maintenance-records-list"), self._maintenance_payload(self.vehicle_disabled.id))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.vehicle_disabled.refresh_from_db()
        self.assertEqual(self.vehicle_disabled.status, VehicleStatus.DISABLED)
        self.assertFalse(MaintenanceRecord.objects.filter(vehicle_id=self.vehicle_disabled.id).exists())

    def test_A_missing_vehicle_field_rejected(self):
        """未指定车辆时拒绝"""
        payload = self._maintenance_payload(self.vehicle_op.id)
        del payload["vehicle"]
        res = self.client.post(reverse("maintenance-records-list"), payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------------- 入口 B：PATCH /api/vehicles/{id}/maintenance/ ----------------

    def test_B_operating_vehicle_can_mark_maintenance(self):
        """运营中车辆可以通过维修快捷入口标记维修"""
        res = self.client.patch(reverse("vehicles-maintenance", args=[self.vehicle_op.id]), {})
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.data)
        self.vehicle_op.refresh_from_db()
        self.assertEqual(self.vehicle_op.status, VehicleStatus.MAINTENANCE)

    def test_B_pending_vehicle_rejected(self):
        """待审核车辆无法通过快捷入口进入维修"""
        res = self.client.patch(reverse("vehicles-maintenance", args=[self.vehicle_pending.id]), {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.vehicle_pending.refresh_from_db()
        self.assertEqual(self.vehicle_pending.status, VehicleStatus.PENDING)

    def test_B_maintenance_vehicle_rejected(self):
        """已在维修车辆无法通过快捷入口重复进入维修"""
        res = self.client.patch(reverse("vehicles-maintenance", args=[self.vehicle_maint.id]), {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.vehicle_maint.refresh_from_db()
        self.assertEqual(self.vehicle_maint.status, VehicleStatus.MAINTENANCE)

    def test_B_disabled_vehicle_rejected(self):
        """停用/报废车辆无法通过快捷入口进入维修"""
        res = self.client.patch(reverse("vehicles-maintenance", args=[self.vehicle_disabled.id]), {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.vehicle_disabled.refresh_from_db()
        self.assertEqual(self.vehicle_disabled.status, VehicleStatus.DISABLED)

    # ---------------- 附加：完整维修流程 ----------------

    def test_full_maintenance_lifecycle(self):
        """完整流程：运营中 -> 创建维修记录 -> 完成维修 -> 运营中"""
        res = self.client.post(reverse("maintenance-records-list"), self._maintenance_payload(self.vehicle_op.id))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        record_id = res.data["id"]

        # 维修中 -> 重复进入被拒
        retry = self.client.patch(reverse("vehicles-maintenance", args=[self.vehicle_op.id]), {})
        self.assertEqual(retry.status_code, status.HTTP_400_BAD_REQUEST)

        # 完成维修
        done = self.client.patch(reverse("maintenance-records-complete", args=[record_id]), {})
        self.assertEqual(done.status_code, status.HTTP_200_OK)
        self.vehicle_op.refresh_from_db()
        self.assertEqual(self.vehicle_op.status, VehicleStatus.OPERATING)

        # 完成后可以再次进入维修
        again = self.client.patch(reverse("vehicles-maintenance", args=[self.vehicle_op.id]), {})
        self.assertEqual(again.status_code, status.HTTP_200_OK)


class OtherBugFixRegressionTests(TestCase):
    """
    回归测试：上一轮其他 bug 的修复结果
    """

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username="admin1", password="p@ss", role=User.Role.ADMIN
        )
        for i, s in enumerate([PileStatus.IDLE, PileStatus.CHARGING, PileStatus.FAULTY, PileStatus.MAINTENANCE]):
            ChargingPile.objects.create(
                code=f"CP{i}",
                location=f"位置{i}",
                lat="31.2304",
                lng="121.4737",
                type=PileType.FAST,
                power="60.00",
                status=s,
                price_per_kwh="1.20",
                installed_at="2025-01-01T00:00:00Z",
            )
        cls.vehicle = Vehicle.objects.create(
            plate_number="沪A-REG01",
            type=VehicleType.TAXI,
            brand="比亚迪",
            model="e6",
            year=2024,
            status=VehicleStatus.OPERATING,
            insurance_expiry=_today(),
        )
        cls.order = TripOrder.objects.create(
            order_no="THREG01",
            user=cls.admin,
            vehicle=cls.vehicle,
            start_location="A",
            end_location="B",
            start_lat="31.2",
            start_lng="121.4",
            end_lat="31.3",
            end_lng="121.5",
            distance=15,
            duration=30,
            fare=0,
            status="ACCEPTED",
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    # Bug1: 地图应展示全部充电桩和真实总数
    def test_bug1_pile_locations_returns_all_statuses(self):
        res = self.client.get(reverse("charging-piles-locations"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        codes = [p["code"] for p in res.data]
        self.assertEqual(len(codes), 4)
        self.assertIn("CP0", codes)  # IDLE
        self.assertIn("CP1", codes)  # CHARGING
        self.assertIn("CP2", codes)  # FAULTY
        self.assertIn("CP3", codes)  # MAINTENANCE

    # Bug3: 订单完成费用应按里程算
    def test_bug3_order_fare_by_distance(self):
        # 先流转到 IN_PROGRESS，再 COMPLETED (ACCEPTED -> IN_PROGRESS -> COMPLETED)
        self.client.patch(
            reverse("orders-status-action", args=[self.order.id]),
            {"status": "IN_PROGRESS"},
        )
        res = self.client.patch(
            reverse("orders-status-action", args=[self.order.id]),
            {"status": "COMPLETED"},
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.data)
        self.order.refresh_from_db()
        self.assertEqual(float(self.order.fare), 15 * 2.40)
